import customtkinter as ctk

class ChatInterface(ctk.CTkFrame):
    def __init__(self, master, state_manager, assistant_callback):
        super().__init__(master)
        self.state_manager = state_manager
        self.assistant_callback = assistant_callback
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.chat_box = ctk.CTkTextbox(self)
        self.chat_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.chat_box.configure(state="disabled")
        
        self.entry = ctk.CTkEntry(self, placeholder_text="Ask Kisan AI for farming advice...")
        self.entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.send_btn = ctk.CTkButton(self, text="Ask AI", command=self.send_message)
        self.send_btn.grid(row=1, column=1, padx=(0,10), pady=10)

        # Bind enter key
        self.entry.bind("<Return>", lambda event: self.send_message())

        self.load_history()

    def load_history(self):
        history = self.state_manager.get_chat_history()
        self.chat_box.configure(state="normal")
        self.chat_box.delete("0.0", "end")
        for msg in history:
            self.chat_box.insert("end", f"{msg['role']}: {msg['message']}\n\n")
        self.chat_box.configure(state="disabled")

    def append_message(self, role, message):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{role}: {message}\n\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")
        self.state_manager.log_chat(role, message)

    def send_message(self):
        user_text = self.entry.get().strip()
        if not user_text: return
        self.entry.delete(0, "end")
        self.send_message_direct(user_text)
        
    def send_message_direct(self, user_text):
        self.append_message("Farmer", user_text)
        
        self.send_btn.configure(state="disabled")
        
        def _get_response():
            # Get response from AI synchronously in this background thread
            response = self.assistant_callback(user_text)
            
            # Post updates safely back to the main UI thread
            self.after(0, lambda: self.append_message("Kisan AI", response))
            self.after(0, lambda: self.send_btn.configure(state="normal"))
            
        import threading
        threading.Thread(target=_get_response, daemon=True).start()

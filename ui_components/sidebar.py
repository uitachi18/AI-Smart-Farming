import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, nav_callback):
        super().__init__(master, width=200, corner_radius=0)
        self.nav_callback = nav_callback
        
        self.grid_rowconfigure(5, weight=1)
        
        self.logo_label = ctk.CTkLabel(self, text="🌱 EdgeFarm AI", 
                                       font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        buttons = ["Dashboard", "Diagnostics", "Resource Optimizer", "Settings"]
        for i, text in enumerate(buttons):
            btn = ctk.CTkButton(self, text=text, fg_color="transparent", 
                                border_width=1, text_color=("gray10", "#DCE4EE"),
                                command=lambda t=text: self.nav_callback(t))
            btn.grid(row=i+1, column=0, padx=20, pady=10, sticky="ew")

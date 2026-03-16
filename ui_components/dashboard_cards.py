import customtkinter as ctk

class SoilWeatherCard(ctk.CTkFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        
        ctk.CTkLabel(self, text="📊 Live Soil & Env Data", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.data_label = ctk.CTkLabel(self, text="Loading...", justify="left")
        self.data_label.pack(pady=10, padx=20, anchor="w")
        
        self.state_manager = state_manager
        self.update_data()

    def update_data(self):
        data = self.state_manager.get_latest_sensor_data()
        text = f"Moisture: {data['moisture']}%\n"
        text += f"Nitrogen: {data['n']} mg/kg\n"
        text += f"Phosphorus: {data['p']} mg/kg\n"
        text += f"Potassium: {data['k']} mg/kg\n"
        text += f"Temp: {data['temp']}°C"
        self.data_label.configure(text=text)

class DiagnosticCard(ctk.CTkFrame):
    def __init__(self, master, state_manager, upload_callback=None):
        super().__init__(master)
        
        self.upload_callback = upload_callback
        
        # Configure grid for the header and button
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        ctk.CTkLabel(self, text="🩺 Recent Diagnostic", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, pady=10, padx=10, sticky="w")
        
        if self.upload_callback:
            self.upload_btn = ctk.CTkButton(self, text="Upload Leaf Image", command=self.upload_callback, width=120)
            self.upload_btn.grid(row=0, column=1, pady=10, padx=10, sticky="e")
        
        self.data_label = ctk.CTkLabel(self, text="Loading...", justify="left", text_color="orange")
        self.data_label.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky="w")
        
        self.state_manager = state_manager
        self.update_data()
        
    def update_data(self):
        data = self.state_manager.get_latest_diagnostic()
        text = f"Crop: {data['crop']}\n"
        text += f"Status: {data['disease']}\n"
        text += f"Confidence: {data['confidence']}%"
        self.data_label.configure(text=text)

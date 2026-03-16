import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from core.state_manager import StateManager
from ui_components.sidebar import Sidebar
from ui_components.dashboard_cards import SoilWeatherCard, DiagnosticCard
from ui_components.chat_interface import ChatInterface
from ai_models.assistant.kisan_ai import LocalAssistant
from ai_models.resources.optimizer import ResourceOptimizer
from ai_models.vision.disease_cnn import CropDiseaseDetector

class SmartFarmingEdge(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.state_manager = StateManager()
        self.assistant = LocalAssistant()
        self.optimizer = ResourceOptimizer()
        
        # Load the locally trained Kaggle weights
        vision_dir = os.path.join(os.path.dirname(__file__), '..', 'ai_models', 'vision')
        model_path = os.path.join(vision_dir, 'offline_weights.pth')
        classes_path = os.path.join(vision_dir, 'classes.json')
        self.vision = CropDiseaseDetector(model_path=model_path, classes_path=classes_path)
        
        # Configure the global theme for a sleek agricultural look
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")
        
        self.title("Edge-AI Smart Farming & Resource Optimizer")
        self.geometry("1100x700")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self._build_sidebar()
        self._build_header()
        self._build_dashboard()

    def nav_callback(self, view):
        print(f"Navigating to {view}")

    def _build_sidebar(self):
        self.sidebar = Sidebar(self, self.nav_callback)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=(20,0))
        
        self.status = ctk.CTkLabel(self.header_frame, text="System: ONLINE | LLM: MOCK | Vision: READY", 
                                   font=ctk.CTkFont(size=14), text_color="green")
        self.status.pack(side="left")

    def handle_chat(self, user_query):
        sensor_data = self.state_manager.get_latest_sensor_data()
        diagnostic_data = self.state_manager.get_latest_diagnostic()
        resource_data = self.optimizer.predict_optimal_resources(
            sensor_data['moisture'], sensor_data['n'], sensor_data['p'], sensor_data['k'], sensor_data['temp']
        )
        return self.assistant.generate_response(user_query, sensor_data, diagnostic_data, resource_data)

    def handle_image_upload(self):
        file_path = ctk.filedialog.askopenfilename(
            title="Select a leaf image to diagnose",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            # Run inference using the CNN
            result = self.vision.infer(file_path)
            
            # Log the new diagnostic to the state manager
            self.state_manager.log_diagnostic("Analyzed Crop", result['condition'], result['confidence'])
            
            # Refresh the card UI
            self.diag_card.update_data()
            
            # Send an automatic message to Kisan AI about the newly uploaded image
            msg = f"I just uploaded an image of my crop. The vision model detected: {result['condition']} with {result['confidence']}% confidence. What should I do?"
            self.chat_card.send_message_direct(msg)

    def _build_dashboard(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        self.main_frame.grid_columnconfigure((0, 1), weight=1)
        self.main_frame.grid_rowconfigure((0, 1), weight=1)
        
        # Panel 1: Soil & Weather Data
        self.soil_card = SoilWeatherCard(self.main_frame, self.state_manager)
        self.soil_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Panel 2: Recent Diagnostics
        self.diag_card = DiagnosticCard(self.main_frame, self.state_manager, upload_callback=self.handle_image_upload)
        self.diag_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Panel 3: AI Chat Interface
        self.chat_card = ChatInterface(self.main_frame, self.state_manager, self.handle_chat)
        self.chat_card.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

if __name__ == "__main__":
    app = SmartFarmingEdge()
    
    # Initialize chat history if empty
    history = app.state_manager.get_chat_history()
    if not history:
        app.state_manager.log_chat("Kisan AI", "Namaste! I noticed your tomato crop has Early Blight and your soil moisture is dropping. I recommend 500ml/sqm of irrigation today and a localized copper fungicide application. How can I help further?")
        app.chat_card.load_history()
        
    app.mainloop()

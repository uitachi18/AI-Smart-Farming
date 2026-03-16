import os
import json
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

class CropDiseaseDetector:
    def __init__(self, model_path=None, classes_path=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load classes dynamically if the JSON exists, otherwise use fallbacks
        self.classes = ['Healthy', 'Tomato Early Blight', 'Potato Late Blight', 'Wheat Rust']
        if classes_path and os.path.exists(classes_path):
            with open(classes_path, 'r') as f:
                self.classes = json.load(f)
        
        num_classes = len(self.classes)
        
        # Using MobileNetV2 for fast, low-power Edge AI inference
        self.model = models.mobilenet_v2(weights=None)
        self.model.classifier[1] = nn.Linear(self.model.classifier[1].in_features, num_classes)
        
        # Load local offline weights if provided
        if model_path and os.path.exists(model_path):
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            except Exception as e:
                print(f"Failed to load weights: {e}. Running with initialized randomly weights.")
                
        self.model.to(self.device)
        self.model.eval()
        
        # Standard ImageNet normalization for PyTorch models
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def infer(self, image_path):
        try:
            image = Image.open(image_path).convert('RGB')
            tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
                confidence, predicted_idx = torch.max(probabilities, 0)
                
            return {
                "condition": self.classes[predicted_idx.item()],
                "confidence": round(confidence.item() * 100, 2)
            }
        except Exception as e:
            print(f"Error during CNN inference: {e}")
            return {"condition": "Unknown", "confidence": 0.0}

if __name__ == "__main__":
    # Test execution
    print("Crop Disease Detector initialized.")

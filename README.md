# Edge-AI Smart Farming & Resource Optimizer

An offline, Edge-AI agricultural assistant and optimizer designed to run locally on hardware like a Raspberry Pi or a laptop. This project directly aligns with SDGs 1, 2, 6, 12, and 13 by optimizing resource use (water, fertilizer) and providing offline, expert AI support to farmers.

## Features
- **Offline LLM Assistant ('Kisan AI')**: Provides expert advice based on real-time sensor data and vision diagnostics without needing a cloud connection.
- **Crop Disease Vision Pipeline**: A PyTorch MobileNetV2 architecture for diagnosing leaf diseases from images locally.
- **Resource Optimizer**: An ML pipeline to predict exact water and fertilizer needs based on dynamic soil conditions to prevent waste.
- **Modern Dark-Mode GUI**: Built with CustomTkinter, featuring real-time data cards, recent diagnostics, and an AI chat interface.
- **Local SQLite State Management**: Logs sensor data and chat histories ensuring zero data leaves the farm.

## Setup Instructions
1. Install requirements:
   `pip install -r requirements.txt`
2. Run the application:
   `python core/app.py`

*(Note: The AI models in `ai_models` currently have mocked generation logic to serve as a prototype that can be easily expanded upon with `llama.cpp` weights and quantized PyTorch `.pt` files.)*

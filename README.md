<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg" alt="PyTorch">
  <img src="https://img.shields.io/badge/CustomTkinter-5.2+-green.svg" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</div>

<br />

<div align="center">
  <h1 align="center">Edge-AI Smart Farming & Resource Optimizer</h1>
  <p align="center">
    <strong>An offline, local-first AI ecosystem for modern agriculture aligned with SDGs 1, 2, 6, 12, and 13.</strong>
  </p>
</div>

---

## 🌾 Overview
The **Edge-AI Smart Farming & Resource Optimizer** is a production-ready agricultural software suite designed to operate entirely offline on farm edge hardware (such as laptops or Raspberry Pi). By leveraging local Large Language Models (LLMs) and optimized Computer Vision pipelines, it provides farmers with real-time agronomy expert advice, predictive resource optimization, and rapid crop disease diagnostics without requiring cloud connectivity.

This project guarantees 100% data privacy—no sensor data or farm diagnostic images ever leave the local machine.

## ✨ Core Features

* **🤖 'Kisan AI' Local Assistant:** A multithreaded, locally hosted LLM (TinyLlama 1.1B parameters) that provides context-aware, empathetic advice based on real-time soil data and diagnosed diseases, ensuring the UI remains responsive even during localized text generation.
* **🍃 Crop Disease Computer Vision Pipeline:** An optimized PyTorch `MobileNetV2` deep learning model trained to rapidly diagnose foliar diseases (e.g., Tomato Early Blight, Potato Late Blight) directly from uploaded leaf imagery.
* **💧 Predictive Resource Optimizer:** A machine learning algorithmic pipeline that continuously processes simulated or real NPK (Nitrogen, Phosphorus, Potassium), Temperature, and Moisture telemetry to deliver surgically precise fertilizer and irrigation quantity recommendations, severely reducing agricultural waste.
* **🖥️ Modern CustomTkinter Dashboard:** A robust, sleek, dark-mode GUI dashboard featuring live telemetry feeds, historic disease diagnostics modules, and a dedicated chat interface with the localized AI.
* **🗄️ Zero-Trust Local State Management:** Utilizes a lightweight SQLite local database architecture to persist sensor logs, chat histories, and vision diagnostics strictly on the edge device.

## 📂 Project Architecture

```text
smart_farming_edge/
├── core/
│   ├── app.py                     # Main application entry point and GUI layout
│   └── state_manager.py           # Local SQLite database initialization and logging
├── ai_models/
│   ├── assistant/
│   │   └── kisan_ai.py            # Multithreaded HuggingFace local LLM pipeline setup
│   ├── resources/
│   │   └── optimizer.py           # Resource prediction algorithms based on NPK/moisture
│   └── vision/
│       ├── disease_cnn.py         # MobileNetV2 PyTorch classification & inference engine
│       └── train_cnn.py           # Utilities for modifying model weights
├── ui_components/
│   ├── chat_interface.py          # Asynchronous Chat GUI for interacting with Kisan AI
│   ├── dashboard_cards.py         # CustomTkinter UI cards for telemetry & vision metrics
│   └── sidebar.py                 # Navigation sidebar 
├── edge_farm.db                   # Local SQLite database (generated at runtime)
├── start_farm.bat                 # Windows execution script
├── requirements.txt               # Ecosystem dependencies
└── README.md                      # Project Documentation
```

## 🚀 Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system. A CUDA-compatible NVIDIA GPU is highly recommended for faster inference, but the application gracefully falls back to CPU processing.

### 2. Clone the Repository
```bash
git clone https://github.com/uitachi18/AI-Smart-Farming.git
cd AI-Smart-Farming
```

### 3. Install Dependencies
Install the required packages using pip:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
You can easily launch the application using the provided batch file or Python executable:

**Windows Command Line:**
```bash
start_farm.bat
```
This batch file will safely spawn the `app.py` process.

**Direct Python Execution:**
```bash
python core/app.py
```

*Note: On first startup, the application may take several minutes to silently download the 1.1B parameter local LLM to your HuggingFace cache. The Graphical Interface will remain fully responsive during this process.*

## 🌍 Sustainable Development Goals (SDGs)
This architecture is inherently scaled to align with international sustainability guidelines:
- **SDG 1 & 2 (No Poverty & Zero Hunger):** Maximizes yield output and directly protects crops from widespread biological diseases via early computer vision detection.
- **SDG 6 (Clean Water & Sanitation):** Strict predictive optimization drastically reduces agricultural water runoff and waste.
- **SDG 12 & 13 (Responsible Consumption & Climate Action):** Prevents systemic over-fertilization (which causes nitrogen soil pollution), lowering the carbon footprint generated by industrial chemical overuse.

## 🤝 Contributing
Contributions are welcome! Please fork the repository and submit a Pull Request. For major feature requests, kindly open an issue first to discuss what you would like to implement.

## 👨‍💻 Creator
Developed by [Gaurav](https://github.com/uitachi18). Feel free to reach out or open an issue if you have questions or suggestions for improving the AI-Smart-Farming project!

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

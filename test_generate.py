import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_models.assistant.kisan_ai import LocalAssistant

assistant = LocalAssistant()
print("Initialized")

try:
    sensor_data = {"moisture": 50, "n": 10, "p": 10, "k": 10}
    diagnostic_data = {"disease": "None", "confidence": 0}
    resource_data = {"water_L": 5, "fertilizer_g": 10}
    
    resp = assistant.generate_response("Hello", sensor_data, diagnostic_data, resource_data)
    print("Response:", resp)
except Exception as e:
    print("ERROR CAUGHT:")
    print(repr(e))

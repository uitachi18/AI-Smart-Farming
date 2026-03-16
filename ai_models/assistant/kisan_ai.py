import torch
from transformers import pipeline

SYSTEM_PROMPT = """You are 'Kisan AI', an expert, highly empathetic, and practical offline AI agricultural assistant. Your goal is to help modern farmers maximize their yield, minimize resource waste, and operate sustainably in alignment with the UN's Sustainable Development Goals (SDGs). 

You operate entirely offline on the farmer's edge device. 

Context of the farm AT THIS EXACT MOMENT:
- Current Soil Moisture: {moisture}%
- Current NPK Levels: N:{n_val}, P:{p_val}, K:{k_val} mg/kg
- Latest Vision Diagnostic: {vision_disease_detected} (Confidence: {vision_confidence}%)
- Resource Optimizer Suggestion: Apply {suggested_water}L of water and {suggested_fertilizer}g of Nitrogen.

Directives:
1. Always base your advice FIRST on the real-time context provided above.
2. Provide practical, step-by-step guidance.
3. Keep your responses concise and highly relevant to the farmer's query. Do not hallucinate external cloud links.
4. Adopt a supportive, respectful tone. Greet the farmer naturally."""

import threading

class LocalAssistant:
    def __init__(self, model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.model_loaded = False
        
        # Load in background so UI isn't blocked
        threading.Thread(target=self._load_model, daemon=True).start()

    def _load_model(self):
        print(f"Initializing Kisan AI Local LLM ({self.model_id}) in background...")
        try:
            self.pipe = pipeline(
                "text-generation", 
                model=self.model_id, 
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32, 
                device_map="auto"
            )
            self.model_loaded = True
            print("\nKisan AI LLM Loaded Successfully.")
        except Exception as e:
            print(f"\nWarning: Could not load the local LLM. {e}")
            self.model_loaded = False

    def generate_response(self, user_query, sensor_data, diagnostic_data, resource_data):
        # Inject dynamic context into the system prompt
        context = SYSTEM_PROMPT.format(
            moisture=sensor_data.get("moisture", 0),
            n_val=sensor_data.get("n", 0),
            p_val=sensor_data.get("p", 0),
            k_val=sensor_data.get("k", 0),
            vision_disease_detected=diagnostic_data.get("disease", "None"),
            vision_confidence=diagnostic_data.get("confidence", 0),
            suggested_water=resource_data.get("water_L", 0),
            suggested_fertilizer=resource_data.get("fertilizer_g", 0)
        )
        
        if self.model_loaded:
            # Format the conversation for the chat model
            messages = [
                {"role": "system", "content": context},
                {"role": "user", "content": user_query},
            ]
            
            prompt = self.pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            
            # Generate response
            outputs = self.pipe(prompt, max_new_tokens=150, max_length=None, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
            
            # Extract just the newly generated text
            full_response = outputs[0]["generated_text"]
            assistant_reply = full_response.split("<|assistant|>")[-1].strip()
            
            return assistant_reply
            
        return "Namaste! I am Kisan AI. My language model is currently initializing or unavailable, but I am here tracking your farm!"

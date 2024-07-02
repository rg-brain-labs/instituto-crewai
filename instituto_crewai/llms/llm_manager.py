from .gemini import Gemini

class LLMManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.models = {
            'gemini': Gemini,            
        }

    def create_llm(self, tipo_modelo, nome_modelo):
        if tipo_modelo not in self.models:
            raise ValueError(f"Model type '{tipo_modelo}' not supported")
        return self.models[tipo_modelo](nome_modelo, self.api_key)

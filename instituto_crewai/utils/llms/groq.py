from enum import Enum

class GroqModels(Enum):
    GEMMA_1_7 = "gemma-7b-it"
    GEMMA_2_9 = "gemma2-9b-it"
    LLMA3_8 = "llama3-8b-8192"
    LLMA3_70 = "llama3-70b-8192"
    LLMA3_1_8 = "llama-3.1-8b-instant"
    LLMA3_1_70 = "llama-3.1-70b-versatile"
    MIXTRAL_8_7 = "mixtral-8x7b-32768"
    LLMA3_GROQ = "llama3-groq-8b-8192-tool-use-preview"
    
    @property
    def max_rpm(self):
        max_rpm_values = {
            "gemma-7b-it": 30,
            "gemma2-9b-it": 30,
            "llama3-70b-8192": 30,
            "llama3-8b-8192": 30,
            "llama-3.1-70b-versatile": 100,
            "llama-3.1-8b-instant": 30,
            "mixtral-8x7b-32768": 30,
            "llama3-groq-8b-8192-tool-use-preview": 30
        }
        return max_rpm_values[self.value]
    
class Groq():
    def __init__(self, modelo):
        self.modelo = modelo        

    def create_instance(self):
        from langchain_groq import ChatGroq
        
        return ChatGroq(
            model=self.modelo.value,
            verbose=True,
            temperature=0.5,
        )
    

from .llm import LLM
from enum import Enum

class GroqModels(Enum):
    GEMMA_1_7 = "gemma-7b-it"
    GEMMA_2_9 = "gemma2-9b-it"
    LLMA3_70 = "llama3-70b-8192"
    LLMA3_8 = "llama3-8b-8192"
    MIXTRAL_8_7 = "mixtral-8x7b-32768"
    
    @property
    def max_rpm(self):
        max_rpm_values = {
            "gemma-7b-it": 30,
            "gemma2-9b-it": 30,
            "llama3-70b-8192": 30,
            "llama3-8b-8192": 30,
            "mixtral-8x7b-32768": 30
        }
        return max_rpm_values[self.value]
    
class Groq(LLM):
    def __init__(self, modelo):
        super().__init__(modelo)        

    def create_instance(self):
        from langchain_groq import ChatGroq
        
        return ChatGroq(
            model=self.modelo.value,
            verbose=True,
            temperature=0.5,
        )

    def generate_text(self, prompt):
        instance = self.create_instance()
        return instance.invoke(prompt).content

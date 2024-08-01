from .llm import LLM
from enum import Enum

class GeminiModels(Enum):
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_1_0_PRO = "gemini-pro"
    
    @property
    def max_rpm(self):
        max_rpm_values = {
            "gemini-1.5-pro": 2,
            "gemini-1.5-flash": 15,
            "gemini-pro": 15
        }
        return max_rpm_values[self.value]
    
class Gemini(LLM):
    def __init__(self, modelo):
        super().__init__(modelo)        

    def create_instance(self):
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        return ChatGoogleGenerativeAI(
            model=self.modelo.value,
            verbose=True,
            temperature=0.5,
        )

    def generate_text(self, prompt):
        instance = self.create_instance()
        return instance.invoke(prompt).content

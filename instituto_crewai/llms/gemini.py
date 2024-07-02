from .llm import LLM
from enum import Enum

class GeminiModels(Enum):
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_1_0_PRO = "gemini-pro"
    
class Gemini(LLM):
    def __init__(self, modelo, api_key):
        super().__init__(modelo)
        self.api_key = api_key

    def create_instance(self):
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        return ChatGoogleGenerativeAI(
            model=self.modelo.value,
            verbose=True,
            temperature=0.5,
            google_api_key=self.api_key
        )

    def generate_text(self, prompt):
        instance = self.create_instance()
        return instance.invoke(prompt).content

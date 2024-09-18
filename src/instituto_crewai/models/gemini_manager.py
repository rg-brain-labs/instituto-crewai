from langchain_google_genai import ChatGoogleGenerativeAI
from .llm_manager import LLMManager

GEMINI_1_5_PRO = "gemini-1.5-pro"
GEMINI_1_5_FLASH = "gemini-1.5-flash"
GEMINI_1_0_PRO = "gemini-1.0-pro"

class GeminiManager(LLMManager):
    """
    Gerenciador de instâncias dos modelos Gemini.
    """

    def __init__(self, temperature: float, model_key: str) -> None:
        models = {
            GEMINI_1_5_PRO: {
                "model_name": GEMINI_1_5_PRO,
                "rpm": 2,
                "verbose": True,
            },
            GEMINI_1_5_FLASH: {
                "model_name": GEMINI_1_5_FLASH,
                "rpm": 15,
                "verbose": True,
            },
            GEMINI_1_0_PRO: {
                "model_name": GEMINI_1_0_PRO,
                "rpm": 15,
                "verbose": True,
            },
        }
        super().__init__(temperature, model_key, models)

    def get_instance(self) -> ChatGoogleGenerativeAI:
        return super().get_instance(ChatGoogleGenerativeAI)

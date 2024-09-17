from langchain_groq import ChatGroq
from llm_manager import LLMManager

GEMMA_1_7 = "gemma-7b-it"
GEMMA_2_9 = "gemma2-9b-it"
LLMA3_8 = "llama3-8b-8192"
LLMA3_70 = "llama3-70b-8192"
LLMA3_1_8 = "llama-3.1-8b-instant"
LLMA3_1_70 = "llama-3.1-70b-versatile"
MIXTRAL_8_7 = "mixtral-8x7b-32768"

class GroqManager(LLMManager):
    """
    Gerenciador de instâncias dos modelos Groq.
    """

    def __init__(self, temperature: float, model_key: str) -> None:
        models = {
            GEMMA_1_7: {
                "model_name": GEMMA_1_7,
                "rpm": 30,
                "verbose": True,
            },
            GEMMA_2_9: {
                "model_name": GEMMA_2_9,
                "rpm": 30,
                "verbose": True,
            },
            LLMA3_8: {
                "model_name": LLMA3_8,
                "rpm": 30,
                "verbose": True,
            },
            LLMA3_70: {
                "model_name": LLMA3_70,
                "rpm": 30,
                "verbose": True,
            },
            LLMA3_1_8: {
                "model_name": LLMA3_1_8,
                "rpm": 30,
                "verbose": True,
            },
            LLMA3_1_70: {
                "model_name": LLMA3_1_70,
                "rpm": 30,
                "verbose": True,
            },
            MIXTRAL_8_7: {
                "model_name": MIXTRAL_8_7,
                "rpm": 30,
                "verbose": True,
            },
        }
        super().__init__(temperature, model_key, models)

    def get_instance(self) -> ChatGroq:
        return super().get_instance(ChatGroq)

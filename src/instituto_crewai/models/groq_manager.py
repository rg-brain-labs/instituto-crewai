from .llm_manager import LLMManager

GEMMA_1_7 = "groq/gemma-7b-it"
GEMMA_2_9 = "groq/gemma2-9b-it"
LLMA3_8 = "groq/llama3-8b-8192"
LLMA3_70 = "groq/llama3-70b-8192"
LLMA3_1_8 = "groq/llama-3.1-8b-instant"
LLMA3_1_70 = "groq/llama-3.1-70b-versatile"
MIXTRAL_8_7 = "groq/mixtral-8x7b-32768"

class GroqManager(LLMManager):
    """
    Gerenciador de instâncias dos modelos Groq.
    """

    def __init__(self, model_key: str) -> None:
        models = {
            GEMMA_1_7: {
                "model_name": GEMMA_1_7,
                "max_rpm": 30,
            },
            GEMMA_2_9: {
                "model_name": GEMMA_2_9,
                "max_rpm": 30,
            },
            LLMA3_8: {
                "model_name": LLMA3_8,
                "max_rpm": 30,
            },
            LLMA3_70: {
                "model_name": LLMA3_70,
                "max_rpm": 30,
            },
            LLMA3_1_8: {
                "model_name": LLMA3_1_8,
                "max_rpm": 30,
            },
            LLMA3_1_70: {
                "model_name": LLMA3_1_70,
                "max_rpm": 30,
            },
            MIXTRAL_8_7: {
                "model_name": MIXTRAL_8_7,
                "max_rpm": 30,
            },
        }
        super().__init__(model_key, models)

    def get_instance(self) -> dict:
        return super().get_instance()

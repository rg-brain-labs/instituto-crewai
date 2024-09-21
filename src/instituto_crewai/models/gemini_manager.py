from instituto_crewai.models.llm_manager import LLMManager

GEMINI_1_5_PRO = "gemini-1.5-pro"
GEMINI_1_5_FLASH = "gemini-1.5-flash"
GEMINI_1_0_PRO = "gemini-1.0-pro"

class GeminiManager(LLMManager):
    """
    Gerenciador de instâncias dos modelos Gemini.
    """

    def __init__(self, model_key: str) -> None:
        models = {
            GEMINI_1_5_PRO: {
                "model_name": GEMINI_1_5_PRO,
                "rpm": 2,
            },
            GEMINI_1_5_FLASH: {
                "model_name": GEMINI_1_5_FLASH,
                "rpm": 15,
            },
            GEMINI_1_0_PRO: {
                "model_name": GEMINI_1_0_PRO,
                "rpm": 15,
            },
        }
        super().__init__(model_key, models)

    def get_instance(self) -> dict:
        return super().get_instance()    

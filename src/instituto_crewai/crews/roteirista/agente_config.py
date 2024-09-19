class AgenteConfig:
    """
    Configuração para um Agente.
    Atributos:
        model_name (str): Nome do modelo de LLM.
        max_rpm (str): Objetivo específico do agente.       
    """
    def __init__(
        self,
        model_name: str,
        max_rpm: str,
    ) -> None:
        self.model_name = model_name
        self.max_rpm = max_rpm

    def __str__(self) -> str:
        return f"AgenteConfig(model_name='{self.model_name}', max_rpm='{self.max_rpm}')"
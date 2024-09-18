from typing import Any, Optional

class AgenteConfig:
    """
    Configuração para um Agente.
    Atributos:
        llm (Any): Instância do LLM (Large Language Model) associada ao agente.
        goal (str): Objetivo específico do agente.
        backstory (str): Backstory específica do agente.
        description (str): Descrição da tarefa específica do agente.
        expected_output (str): Saída esperada da tarefa do agente.
    """
    def __init__(
        self,
        llm: Optional[Any],
        goal: str = "",
        backstory: str = "",
        description: str = "",
        expected_output: str = "",
    ) -> None:
        self.llm = llm
        self.goal = goal
        self.backstory = backstory
        self.description = description
        self.expected_output = expected_output
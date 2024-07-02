# agentes/agente.py

class Agente:
    def __init__(self, role, goal, backstory, verbose, llm, tools, allow_delegation):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self.llm = llm
        self.tools = tools
        self.allow_delegation = allow_delegation

    def perform_task(self, task_details):
        # Método genérico para realizar uma tarefa
        raise NotImplementedError("Este método deve ser implementado por subclasses")

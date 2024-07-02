class Task:
    def __init__(self, description, expected_output, agent, verbose=0):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.verbose = verbose

    def execute(self, **kwargs):
        # Método genérico para executar a tarefa
        raise NotImplementedError("Este método deve ser implementado por subclasses")

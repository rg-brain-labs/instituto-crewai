from .task import Task

class PesquisaTask(Task):
    def __init__(self, agent, verbose=2):
        description = "Pesquise as últimas tendências sobre {topic}."
        expected_output = """
            Um relatório detalhado sobre as tendências mais recentes sobre {topic} 
            na área de tecnologia.
            """
        super().__init__(description, expected_output, agent, verbose)
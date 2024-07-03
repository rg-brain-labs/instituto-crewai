from .task import Task

class CriacaoImagemTask(Task):
    def __init__(self, agent, verbose=2):
        description="""
                Crie {n} prompts para criar uma imagem atraente para 
                acompanhar a postagem no Instagram sobre {topic}.
            """
        expected_output="""
                {n} prompts de alta qualidade adequados para o 
                Instagram based em {topic}.
            """
        super().__init__(description, expected_output, agent, verbose)

    def create(self):
        return self.create_task()

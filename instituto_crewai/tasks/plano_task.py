from .task import Task

class PlanoTask(Task):
    def __init__(self, agent, verbose=2):
        description="""
                1. Priorize as últimas tendências, principais 'players', 
                    e notícias relevantes sobre {topic}. 
                2. Identifique o público-alvo, considerando 
                    seus interesses e pontos de dor. 
                3. Desenvolva um plano de conteúdo detalhado, incluindo  
                    uma introdução, pontos principais e um chamado à ação.
                4. Inclua palavras-chave de SEO e dados ou fontes relevantes.          
            """
        expected_output = """
                1. Priorize as últimas tendências, principais 'players', Um 
                    documento de plano de conteúdo para {n} posts sobre {topic}
                    com um esboço, análise do público, palavras-chave de SEO e recursos.
            """
        super().__init__(description, expected_output, agent, verbose)

    def create(self):
        return self.create_task()

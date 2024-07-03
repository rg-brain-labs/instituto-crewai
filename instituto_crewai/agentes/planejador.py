from .agente import Agente
from textwrap import dedent

class Planejador(Agente):
    def __init__(self, llm, tools):
        super().__init__(
            role="Planejador de postagens",
            goal="Planejar conteúdo envolvente para Instagram sobre {topic}.",
            backstory=dedent("""
                    Você está trabalhando no planejamento de {n} posts 
                    para o Instagram sobre o tema: {topic}. 
                    Você coleta informações que ajudam o 
                    público se informar sobre {topic}. 
                    Seu trabalho é a base para que 
                    o Pesquisador de Conteúdo procure na web sobre {topic}.            
                """),
            verbose=True,
            llm=llm,
            tools=tools,
            allow_delegation=False
        )

    def create(self):        
        return self.create_agente()

from .agente import Agente
from textwrap import dedent

class Pesquisador(Agente):
    def __init__(self, llm, tools):
        super().__init__(
            role="Pesquisador",
            goal=dedent("""
                    Pesquisar tendências para postagens sobre {topic} na 
                    área de tecnologia que possam ser usadas pelo Planejador.
                    Seu trabalho é a base para que o escritor possa escrever 
                    {n} posts sobre {topic}.
                """),
            backstory=dedent("""
                    Você é um pesquisador experiente, sempre em busca das últimas 
                    tendências e informações relevantes sobre {topic}.
                """),
            verbose=True,
            llm=llm,
            tools=tools,
            allow_delegation=False
        )

    def create(self):
        return self.create_agente()

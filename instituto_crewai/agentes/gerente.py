from crewai import Agent
from textwrap import dedent

class Gerente():
    def __init__(self, llm):        
        self.role="Gerente de postagens"
        self.goal=dedent(
            """
                Supervisione o trabalho de uma equipe de postagens no Instagram. 
                Você é bem crítico em relação ao que vai ser postado no Instagram 
                da empresa de notícias na área da tecnologia.
                Você delegará tarefas à sua equipe e fará perguntas esclarecedoras
                para revisar e aprovar as {n} posts sobre {topic} que foram solicitadas 
                pela direção da empresa.
            """)
        self.backstory=dedent(
            """
                Você é um gerente experiente, sempre em busca das últimas tendências 
                e informações relevantes.
                Você está trabalhando com uma nova demanda e faz com que sua equipe 
                realize o trabalho da melhor forma possível.
            """)
        self.verbose=True
        self.llm=llm       
        self.allow_delegation=True
        
    def criar_agente(self):
        return Agent(
            role = self.role,
            goal = self.goal,
            backstory = self.backstory,
            llm=self.llm,
            verbose=self.verbose,
            allow_delegation=self.allow_delegation
        )
       
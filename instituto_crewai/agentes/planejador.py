from crewai import Agent
from textwrap import dedent

class Planejador():
    def __init__(self, llm):        
        self.role = "Planejador de postagens"
        self.goal = "Planejar conteúdo envolvente para Instagram sobre {topic}."
        self.backstory = dedent("""
                Você está trabalhando no planejamento de {n} posts 
                para o Instagram sobre o tema: {topic}. 
                Você coleta informações que ajudam o 
                público se informar sobre {topic}. 
                Seu trabalho é a base para que 
                o Pesquisador de Conteúdo procure na web sobre {topic}.            
            """)
        self.verbose = True
        self.llm = llm        
        self.allow_delegation = False
        
    def criar_agente(self):       
        return Agent(
            role = self.role,
            goal = self.goal,
            backstory = self.backstory,
            llm = self.llm,
            verbose = self.verbose,
            allow_delegation = self.allow_delegation
        )
        
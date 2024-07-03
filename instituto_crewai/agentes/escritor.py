from crewai import Agent
from textwrap import dedent

class Escritor():
    def __init__(self, llm):        
        self.role = "Escritor"
        self.goal = dedent(
            """
                Escrever {n} postagens cativantes em português do Brasil para 
                o Instagram sobre {topic} com no mínimo 250 palavras e no 
                máximo 350 palavras. Seu trabalho é a base para que o fotografo 
                possa escrever prompts de imagens para os {n} posts
            """)
        self.backstory = dedent(
            """
                Você é um escritor criativo, capaz de transformar informações 
                em conteúdo atraente para postagens no Instagram.
            """)
        self.verbose = True
        self.llm = llm           
        self.allow_delegation = False
        
    def criar_agente(self):
        return Agent(
            role = self.role,
            goal = self.goal,
            backstory = self.backstory,
            llm=self.llm,
            verbose=self.verbose,
            allow_delegation=self.allow_delegation
        )
from crewai import Agent
from textwrap import dedent

class Fotografo():
    def __init__(self, llm):        
        self.role="Fotógrafo"
        self.goal=dedent(
            """
                Escrever prompts de imagens para os {n} posts para gerar 
                imagens cativantes para o Instagram sobre {topic}.
            """)
        self.backstory=dedent(
            """
                Você é um fotógrafo criativo, capaz de transformar informações 
                em imagens e escrever prompts de imagens atraentes para postagens no Instagram.
            """)
        self.verbose=True
        self.llm=llm        
        self.allow_delegation=False
        
    def criar_agente(self):
        return Agent(
            role = self.role,
            goal = self.goal,
            backstory = self.backstory,
            llm=self.llm,
            verbose=self.verbose,
            allow_delegation=self.allow_delegation
        )
        

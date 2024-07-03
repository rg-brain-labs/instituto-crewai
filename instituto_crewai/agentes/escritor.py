from .agente import Agente
from textwrap import dedent

class Escritor(Agente):
    def __init__(self, llm, tools):
        super().__init__(
            role="Escritor",
            goal=dedent(
                """
                    Escrever {n} postagens cativantes em português do Brasil para 
                    o Instagram sobre {topic} com no mínimo 250 palavras e no 
                    máximo 350 palavras. Seu trabalho é a base para que o fotografo 
                    possa escrever prompts de imagens para os {n} posts
                """),
            backstory=dedent(
                """
                    Você é um escritor criativo, capaz de transformar informações 
                    em conteúdo atraente para postagens no Instagram.
                """),
            verbose=True,
            llm=llm,
            tools=tools,
            allow_delegation=False
        )

    def create(self):
        return self.create_agente()

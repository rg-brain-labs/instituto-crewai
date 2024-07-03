from .agente import Agente
from textwrap import dedent

class Fotografo(Agente):
    def __init__(self, llm, tools):
        super().__init__(
            role="Fotógrafo",
            goal=dedent(
                """
                    Escrever prompts de imagens para os {n} posts para gerar 
                    imagens cativantes para o Instagram sobre {topic}.
                """),
            backstory=dedent(
                """
                    Você é um fotógrafo criativo, capaz de transformar informações 
                    em imagens e escrever prompts de imagens atraentes para postagens no Instagram.
                """),
            verbose=True,
            llm=llm,
            tools=tools,
            allow_delegation=False
        )

    def create(self):
        return self.create_agente()

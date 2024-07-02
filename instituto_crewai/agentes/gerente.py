from .agente import Agente

class Gerente(Agente):
    def __init__(self, llm, tools):
        super().__init__(
            role="Gerente de postagens",
            goal="Supervisionar o trabalho de uma equipe de postagens no Instagram. Você é bem crítico em relação à qualidade e relevância das postagens em áreas de notícias na área da tecnologia.",
            backstory="Você está trabalhando com uma nova demanda e faz com que sua equipe realize o trabalho da melhor forma possível.",
            verbose=True,
            llm=llm,
            tools=tools,
            allow_delegation=True
        )

    def perform_task(self, topic, n):
        # Implementar a lógica para gerenciar a equipe de postagens
        return f"Supervisionando a criação de {n} posts sobre {topic}."

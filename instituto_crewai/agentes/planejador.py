from .agente import Agente

class Planejador(Agente):
    def __init__(self, llm, tools):
        super().__init__(
            role="Planejador de postagens",
            goal="Planejar conteúdo envolvente para Instagram sobre {topic}.",
            backstory="Você está trabalhando no planejamento de {n} posts para o Instagram sobre o tema: {topic}.",
            verbose=True,
            llm=llm,
            tools=tools,
            allow_delegation=False
        )

    def perform_task(self, topic, n):
        # Implementar a lógica para planejar posts
        return f"Planejando {n} posts sobre {topic}."

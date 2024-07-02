from .agente import Agente

class Pesquisador(Agente):
    def __init__(self, llm, tools):
        super().__init__(
            role="Pesquisador",
            goal="Pesquisar tendências para postagens sobre {topic} na área de tecnologia que possam ser usadas pelo Planejador.",
            backstory="Você é um pesquisador experiente, sempre em busca das últimas tendências e informações relevantes sobre {topic}.",
            verbose=True,
            llm=llm,
            tools=tools,
            allow_delegation=False
        )

    def perform_task(self, topic, n):
        # Implementar a lógica para pesquisar tendências
        return f"Pesquisando {n} tendências sobre {topic}."

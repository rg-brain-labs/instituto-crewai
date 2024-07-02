from .agente import Agente

class Escritor(Agente):
    def __init__(self, llm, tools):
        super().__init__(
            role="Escritor",
            goal="Escrever {n} postagens cativantes em português do Brasil para o Instagram sobre {topic} com no mínimo 250 palavras e no máximo 350 palavras.",
            backstory="Você é um escritor criativo, capaz de transformar informações em conteúdo atraente para postagens no Instagram.",
            verbose=True,
            llm=llm,
            tools=tools,
            allow_delegation=False
        )

    def perform_task(self, topic, n):
        # Implementar a lógica para escrever postagens
        return f"Escrevendo {n} postagens sobre {topic}."

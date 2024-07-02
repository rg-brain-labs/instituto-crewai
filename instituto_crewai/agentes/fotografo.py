from .agente import Agente

class Fotografo(Agente):
    def __init__(self, llm, tools):
        super().__init__(
            role="Fotógrafo",
            goal="Escrever prompts de imagens para os {n} posts para gerar imagens cativantes para o Instagram sobre {topic}.",
            backstory="Você é um fotógrafo criativo, capaz de transformar informações em imagens e escrever prompts de imagens atraentes para postagens no Instagram.",
            verbose=True,
            llm=llm,
            tools=tools,
            allow_delegation=False
        )

    def perform_task(self, topic, n):
        # Implementar a lógica para escrever prompts de imagens
        return f"Escrevendo {n} prompts de imagens sobre {topic}."

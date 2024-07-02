from textwrap import dedent
from .task import Task

class EscritaTask(Task):
    def __init__(self, agent, verbose=2):
        description = dedent("""Escreva {n} postagens envolventes em português do Brasil
                        com base nas tendências pesquisadas sobre {topic} com no mínimo 250 palavras e no máximo 350 palavras cada.
                        Cada post deve ser formatado como:
                        \n\nPOST:\ntexto do post em português do brasil
                        \n\nPROMPT:\nPrompt da imagem desse post\n\n""")
        expected_output = "{n} postagens de Instagram bem escritas, atraentes e em português do Brasil, formatadas conforme especificado para o tópico {topic}."
        super().__init__(description, expected_output, agent, verbose)

    def execute(self, topic, n):
        # Implementar a lógica para executar a tarefa
        return self.agent.perform_task(topic, n)

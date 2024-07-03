from .task import Task

class RevisaoTask(Task):
    def __init__(self, agent, verbose=2):
        description="""
                Revise as {n} escritas e prompts de imagens
                para as {n} postagens do cliente e garanta
                que as informações de cada postagem estejam
                organizadas, sem erros e cativantes
                em português do Brasil sobre {topic}.
                Certifique-se de que cada post está formatado como:
                
                \n\nPOST:\ntexto do post em português do brasil
                \n\nPROMPT:\nPrompt da imagem desse post\n\n
            """
        expected_output="""
                {n} textos e prompts de imagens organizados por 
                post, revisados e prontos para serem publicados 
                em português do Brasil, formatados conforme 
                especificado.
            """
        super().__init__(description, expected_output, agent, verbose)
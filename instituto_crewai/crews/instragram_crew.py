import os

from crewai_tools.tools.scrape_website_tool.scrape_website_tool import ScrapeWebsiteTool
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from textwrap import dedent

class InstagramCrew():
    def __init__(self, llm):
        # Criando as Tools
        ainew = ScrapeWebsiteTool(
            website_url="https://www.artificialintelligence-news.com/"
        )
        forbes = ScrapeWebsiteTool(
            website_url="https://www.forbes.com/ai/"
        )
        
        # Criando os Agents
        planejador = Agent(
            role="Planejador de postagem",
            goal="Planejar conteúdo envolvente para instagram sobre {topic}",
            backstory="Você está trabalhando no planejamento de {n} posts para o instagram "
                    "sobre o tema: {topic}. "
                    "Você coleta informações que ajudam o "
                    "público se informar sobre {topic}. "
                    "Seu trabalho é a base para que "
                    "o Pesquisador de Conteúdo procure na web sobre {topic}.",
            verbose=True,
            llm=llm,
            allow_delegation=False

        )
        
        pesquisador = Agent(
            role='Pesquisador',
            goal='Pesquisar tendências para postagens sobre {topic} na área '
                'de tecnologia com base no planejamento do Planejador. '
                'Seu trabalho é a base para que '
                'o escritor possa escrever {n} posts sobre {topic}',
            verbose=True,
            backstory="Você é um pesquisador experiente, sempre em busca das últimas tendências e informações relevantes sobre {topic}.",
            llm=llm,
            tools=[ainew, forbes],
            allow_delegation=False
        )        
        
        escritor = Agent(
            role='Escritor',
            goal='Escrever {n} postagens cativantes em português do Brasil para o Instagram sobre {topic} com no mínimo 250 palavras e no máximo 350 palavras.'
                'Seu trabalho é a base para que o fotografo possa escrever prompts de imagens para os {n} posts',
            backstory="Você é um escritor criativo, capaz de transformar informações em conteúdo atraente para postagens no Instagram.",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        
        
        fotografo = Agent(
            role='Fotógrafo',
            goal='Escrever prompts de imagens para as {n} postagens para gerar imagens cativantes para o Instagram sobre {topic}.',
            backstory=dedent("""Você é um fotógrafo criativo,
                                capaz de transformar informações em imagens e escrever prompts
                                de imagens atraentes para postagens no Instagram."""),
            verbose=True,
            llm=llm,
            max_rpm=1,
            allow_delegation=False
        )
        gerente = Agent(
            role='Gerente de postagens',
            goal=dedent("""Supervisione o trabalho de uma equipe de postagens no Instagram. Você é bem crítico em relação
                    ao que vai ser postado no Instagram da empresa de notícias na área da tecnologia.
                    Você delegará tarefas à sua equipe e fará perguntas esclarecedoras
                    para revisar e aprovar as {n} posts sobre {topic} que foram solicitadas pela direção da empresa."""),
            verbose=True,
            backstory=dedent("""Você é um gerente experiente, sempre em busca das últimas tendências e informações relevantes.
                        Você está trabalhando com uma nova demanda e faz com que sua equipe realize o trabalho da
                        melhor forma possível."""),
            llm=llm,
        )
        
        # Criando as Taks
        plano_task = Task(
            description=(
                "1. Priorize as últimas tendências, principais 'players', "
                    "e notícias relevantes sobre {topic}.\n"
                "2. Identifique o público-alvo, considerando "
                    "seus interesses e pontos de dor.\n"
                "3. Desenvolva um plano de conteúdo detalhado, incluindo "
                    "uma introdução, pontos principais e um chamado à ação.\n"
                "4. Inclua palavras-chave de SEO e dados ou fontes relevantes."
            ),
            expected_output="Um documento de plano de conteúdo para {n} posts sobre {topic} "
                "com um esboço, análise do público, "
                "palavras-chave de SEO e recursos.",
            agent=planejador,
            verbose=2
        )
        
        pesquisa_task = Task(
            description="Pesquise as últimas tendências sobre {topic}.",
            expected_output="Um relatório detalhado sobre as tendências mais recentes sobre {topic} na área de tecnologia.",
            agent=pesquisador,
            verbose=2
        )
        
        escrita_task = Task(
            description=dedent("""Escreva {n} postagens envolventes em português do Brasil
                                com base nas tendências pesquisadas sobre {topic} com no mínimo 250 palavras e no máximo 350 palavras cada.
                                Cada post deve ser formatado como:
                                \n\nPOST:\ntexto do post em português do brasil
                                \n\nPROMPT:\nPrompt da imagem desse post\n\n"""),
            expected_output="{n} postagens de Instagram bem escritas, atraentes e em português do Brasil, formatadas conforme especificado para o tópico {topic}.",
            agent=escritor,
            verbose=2
        )
        
        criacao_imagem_task = Task(
            description="Crie {n} prompts para criar uma imagem atraente para acompanhar a postagem no Instagram sobre {topic}.",
            expected_output="{n} prompts de alta qualidade adequados para o Instagram based in {topic}.",
            agent=fotografo,
            verbose=2
        )
        
        revisao_task = Task(
            description=dedent("""Revise as {n} escritas e prompts de imagens
                                para as {n} postagens do cliente e garanta
                                que as informações de cada postagem estejam organizadas, sem erros e cativantes
                                em português do Brasil sobre {topic}.
                                Certifique-se de que cada post está formatado como:
                                \n\nPOST:\ntexto do post em português do brasil
                                \n\nPROMPT:\nPrompt da imagem desse post\n\n"""),
            expected_output="{n} textos e prompts de imagens organizados por post, revisados e prontos para serem publicados em português do Brasil, formatados conforme especificado.",
            agent=gerente,
            verbose=2
        )
        
        # Criando a Crew
        self.crew = Crew(
            agents=[planejador, pesquisador, escritor, fotografo, gerente],
            tasks=[plano_task, pesquisa_task, escrita_task, criacao_imagem_task, revisao_task],
            process=Process.sequential,
            verbose=2,
            memory=True,
            
        )
    
    def run(self):
        result = self.crew.kickoff(
            inputs={
                'topic':'Inteligência Artificial e Agentes Inteligêntes',
                'n':1
            })
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"posts-{current_date}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(result)
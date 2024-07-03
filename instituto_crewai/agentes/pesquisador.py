from crewai import Agent
from textwrap import dedent
from tools.scraping import AINewScraper, ForbesScraper

class Pesquisador():
    def __init__(self, llm, tools):       
        self.role = "Pesquisador"
        self.goal = dedent("""
                Pesquisar tendências para postagens sobre {topic} na 
                área de tecnologia que possam ser usadas pelo Planejador.
                Seu trabalho é a base para que o escritor possa escrever 
                {n} posts sobre {topic}.
            """)
        self.backstory = dedent("""
                Você é um pesquisador experiente, sempre em busca das últimas 
                tendências e informações relevantes sobre {topic}.
            """)
        self.verbose = True
        self.llm = llm
        self.tools = tools
        self.allow_delegation = False
        
    def criar_agente(self):   
        # Criando as Tools
        ainew_scraper = AINewScraper().create_scraper_tool()
        forbes_scraper = ForbesScraper().create_scraper_tool()
             
        return Agent(
            role = self.role,
            goal = self.goal,
            backstory = self.backstory,
            llm = self.llm,
            verbose = self.verbose,
            tools = [ainew_scraper, forbes_scraper],
            allow_delegation = self.allow_delegation,
        )
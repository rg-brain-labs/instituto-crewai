from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools.scrape_website_tool.scrape_website_tool import ScrapeWebsiteTool
from llms import Gemini, Groq, GeminiModels, GroqModels
from dotenv import load_dotenv
from pathlib import Path

# Carrega variáveis de ambiente
dotenv_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(dotenv_path)

ainew = ScrapeWebsiteTool(
    website_url="https://www.artificialintelligence-news.com/"
)

forbes = ScrapeWebsiteTool(
    website_url="https://www.forbes.com/ai/"
)



@CrewBase
class InstagramCrew():
    
    def __init__(self) -> None:
        gemini = Gemini(GeminiModels.GEMINI_1_5_PRO)
        groq = Groq(GroqModels.LLMA3_8)
        
        self.gemini_llm = gemini.create_instance()
        self.gemini_max_rpm = GeminiModels.GEMINI_1_5_PRO.max_rpm
        
        self.llam3_llm = groq.create_instance()
        self.llam3_max_rpm = GroqModels.LLMA3_8.max_rpm
       
        
    agents_config = '../config/agents.yaml'
    tasks_config = '../config/tasks.yaml'
 
    @agent
    def planejador(self) -> Agent:
        return Agent(
            config=self.agents_config['planejador_instagram'],            
            verbose=True,
            llm=self.llam3_llm,
            allow_delegation=False,
            max_rpm=self.llam3_max_rpm,
        )
        
    @agent
    def pesquisador(self) -> Agent:
        return Agent(
            config=self.agents_config['pesquisador_instagram'],            
            verbose=True,
            llm=self.llam3_llm,
            allow_delegation=False,
            tools=[ainew, forbes],
            max_rpm=self.llam3_max_rpm,
        )
        
    @agent
    def escritor(self) -> Agent:
        return Agent(
            config=self.agents_config['escritor_instagram'],            
            verbose=True,
            llm=self.gemini_llm,
            allow_delegation=False,
            max_rpm=self.gemini_max_rpm,
        )
        
    @agent
    def fotografo(self) -> Agent:
        return Agent(
            config=self.agents_config['fotografo_instagram'],            
            verbose=True,
            llm=self.llam3_llm,
            allow_delegation=False,
            max_rpm=self.llam3_max_rpm,
        )
        
    @agent
    def gerente(self) -> Agent:
        return Agent(
            config=self.agents_config['gerente_instagram'],            
            verbose=True,
            llm=self.gemini_llm, 
            max_rpm=self.gemini_max_rpm,  
            allow_delegation=False        
        )
        
    @task
    def plano_task(self) -> Task:
        return Task(
            config=self.tasks_config['plano_task'],
            agent=self.planejador(),
            verbose=2,
        )
        
    @task
    def pesquisa_task(self) -> Task:
        return Task(
            config=self.tasks_config['pesquisa_task'],
            agent=self.pesquisador(),
            verbose=2
        )
        
    @task
    def escrita_task(self) -> Task:
        return Task(
            config=self.tasks_config['escrita_task'],
            agent=self.escritor(),
            verbose=2
        )
        
    @task
    def criacao_imagem_task(self) -> Task:
        return Task(
            config=self.tasks_config['criacao_imagem_task'],
            agent=self.fotografo(),
            verbose=2
        )
        
    @task
    def revisao_task(self) -> Task:
        return Task(
            config=self.tasks_config['revisao_task'],
            agent=self.gerente(),
            verbose=2
        )
        
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=2,
            language="pt-br",
            memory=True,
            embedder = {
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",        
                }
            },
        )
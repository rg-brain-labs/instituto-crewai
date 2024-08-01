from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools.scrape_website_tool.scrape_website_tool import ScrapeWebsiteTool
from crewai_tools import BaseTool
from crewai_tools import DirectoryReadTool, FileReadTool
from llms import Gemini, Groq, GeminiModels, GroqModels
from dotenv import load_dotenv
from pathlib import Path
import json

# Carrega variáveis de ambiente
dotenv_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(dotenv_path)

class SearchTool(BaseTool):
    name: str = ("Ferramenta para busca de sites")
    description: str = ("Retorna um JSON com os sites das empresas.")
    
    def _run(self) -> str:
        return json.dumps({
            "results": [
                {
                    "description": "A AetherTech é uma empresa líder em tecnologia de energia espacial, desenvolvendo soluções sustentáveis e inovadoras para o futuro.  A empresa está construindo uma infraestrutura de energia solar orbital,  oferecendo  uma  fonte limpa e ininterrupta de energia  para  o  planeta.",
                    "url": "http://127.0.0.1:5000/aether-tech"
                },
                {
                    "description": "Solaris Ventures está  revolucionando  o  turismo  espacial  com  o  primeiro  hotel  espacial  de  luxo  do  mundo,  oferecendo  experiências  inesquecíveis  para  quem  busca  aventuras  interestelares  em  um  ambiente  único  e  luxuoso.",
                    "url": "http://127.0.0.1:5000/solaris-ventures"
                }
            ]
        })

directory_read_tool = DirectoryReadTool(directory='./instrucoes')
file_read_tool = FileReadTool()
search_tool = SearchTool()
scrape_tool = ScrapeWebsiteTool()
scrape_zenith_voyages = ScrapeWebsiteTool(website_url='http://127.0.0.1:5000/zenith-voyages')

@CrewBase
class CampanhaCrew():
    
    def __init__(self) -> None:
        gemini = Gemini(GeminiModels.GEMINI_1_5_PRO)
        groq = Groq(GroqModels.LLMA3_8)
        
        self.gemini_llm = gemini.create_instance()
        self.gemini_max_rpm = GeminiModels.GEMINI_1_5_PRO.max_rpm
        
        self.llam3_llm = groq.create_instance()
        self.llam3_max_rpm = GroqModels.LLMA3_8.max_rpm    
 
    @agent   
    def representante_vendas(self) -> Agent:
        return Agent(            
            role="Representante de Vendas",
            goal="Identificar leads de alto valor que correspondam "
                "ao nosso perfil de cliente ideal",
            backstory=(
                "Como parte da dinâmica equipe de vendas da Zenith Voyages, "
                "sua missão é vasculhar "
                "o cenário digital em busca de leads potenciais. "
                "Armado com ferramentas de ponta "
                "e uma mentalidade estratégica, você analisa dados, "
                "tendências e interações para "
                "descobrir oportunidades que outros possam ter negligenciado. "
                "Seu trabalho é crucial para abrir caminho "
                "para engajamentos significativos e impulsionar o crescimento da empresa."
            ),
            memory=True,   
            verbose=True,
            llm=self.llam3_llm,
            allow_delegation=False,
            max_rpm=self.llam3_max_rpm,
        )
        
    @agent   
    def lider_vendas(self) -> Agent:
        return Agent(            
            role="Líder de Vendas",
            goal="Cultivar leads com comunicações personalizadas e cativantes",
            backstory=(
                "Dentro do vibrante ecossistema do departamento de vendas da CrewAI, "
                "você se destaca como a ponte entre os clientes potenciais "
                "e as soluções que eles precisam."
                "Criando mensagens envolventes e personalizadas, "
                "você não apenas informa os leads sobre nossas ofertas "
                "mas também os faz sentir vistos e ouvidos."
                "Seu papel é crucial para converter interesse "
                "em ação, guiando os leads na jornada "
                "da curiosidade ao compromisso."
            ),
            memory=True,
            verbose=True,
            llm=self.llam3_llm,
            allow_delegation=False,
            max_rpm=self.llam3_max_rpm,
        )
        
    @task
    def representante_vendas_task(self) -> Task:
        return Task(
            description=(
                "Conduza uma análise aprofundada de {lead_name}, "
                "uma empresa no setor de {industry} "
                "que recentemente demonstrou interesse em nossas soluções. "
                "Utilize todas as fontes de dados disponíveis "
                "para compilar um perfil detalhado, "
                "focando em principais tomadores de decisão, desenvolvimentos recentes da empresa "
                "e necessidades potenciais "
                "que se alinhem com nossas ofertas. "
                "Esta tarefa é crucial para adaptar "
                "nossa estratégia de engajamento de forma eficaz.\n"
                "Não faça suposições e "
                "use apenas informações das quais você tem absoluta certeza.\n"
                "Para saber mais sobre a empresa em que você atua pode usar a ferramenta scrape_zenith_voyages"
            ),
            expected_output=(
                "Um relatório abrangente sobre {lead_name}, "
                "incluindo histórico da empresa, "
                "principais funcionários, marcos recentes e necessidades identificadas. "
                "Destaque as áreas potenciais onde "
                "nossas soluções podem fornecer valor "
                "e sugira estratégias de engajamento personalizadas."
            ),
            tools=[directory_read_tool, file_read_tool, search_tool, scrape_zenith_voyages],
            agent=self.representante_vendas,
            verbose=2,
        )
        
    @task
    def lider_vendas_task(self) -> Task:
        return Task(
            description=(
                "Usando os insights obtidos do "
                "relatório de perfil de lead sobre {lead_name}, "
                "crie uma campanha de contato personalizada "
                "direcionada a {key_decision_maker}, "
                "o(a) {position} de {lead_name}. "
                "A campanha deve abordar o recente {milestone} deles "
                "e como nossas soluções podem apoiar seus objetivos. "
                "Sua comunicação deve ressoar "
                "com a cultura e os valores da empresa {lead_name}, "
                "demonstrando um profundo entendimento "
                "do negócio e das necessidades deles.\n"
                "Não faça suposições e use apenas "
                "informações das quais você tem absoluta certeza."
            ),
            expected_output=(
                "Uma série de rascunhos de e-mails personalizados "
                "adaptados para {lead_name}, "
                "especificamente direcionados a {key_decision_maker}."
                "Cada rascunho deve incluir "
                "uma narrativa envolvente que conecte nossas soluções "
                "com as conquistas recentes e os objetivos futuros deles. "
                "Garanta que o tom seja envolvente, profissional "
                "e alinhado com a identidade corporativa de {lead_name}."
            ),
            tools=[search_tool],
            agent=self.lider_vendas,
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
            # memory=True,
            # embedder = {
            #     "provider": "google",
            #     "config": {
            #         "model": "models/text-embedding-004",        
            #     }
            # },
        )
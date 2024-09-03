from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq

from crewai_tools import ScrapeWebsiteTool
from langchain_community.tools import DuckDuckGoSearchResults
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from pathlib import Path

# Carrega variáveis de ambiente
dotenv_path = Path(__file__).parent.parent.parent / 'config' / '.env'
load_dotenv(dotenv_path)

class EstrategiaMercado(BaseModel):
    """Modelo de estratégia de mercado"""
    nome: str = Field(..., description="Nome da estratégia de mercado")
    taticas: List[str] = Field(..., description="Lista de táticas a serem usadas na estratégia de mercado")
    canais: List[str] = Field(..., description="Lista de canais a serem usados na estratégia de mercado")
    KPIs: List[str] = Field(..., description="Lista de KPIs a serem usados na estratégia de mercado")

class IdeiaCampanha(BaseModel):
    """Modelo de ideia de campanha"""
    nome: str = Field(..., description="Nome da ideia de campanha")
    descricao: str = Field(..., description="Descrição da ideia de campanha")
    publico: str = Field(..., description="Público da ideia de campanha")
    canal: str = Field(..., description="Canal da ideia de campanha")

class TextoPublicitario(BaseModel):
    """Modelo de texto publicitário"""
    titulo: str = Field(..., description="Título do texto publicitário")
    corpo: str = Field(..., description="Corpo do texto publicitário")

search_tool = DuckDuckGoSearchResults(backend="text", max_results=5)

@CrewBase
class PostMarketigCrew():
	"""PostMarketig crew"""

	llam3_llm = ChatGroq(
		model='llama3-8b-8192',
		verbose=True,
		temperature=0.5
	)
    
    # llam3_llm = ChatGroq(
	# 	model='llama3-8b-8192',
	# 	verbose=True,
	# 	temperature=0.5,
	# 	)
	# llam3_max_rpm = 20

	agents_config = 'config/agentes.yaml'
	tasks_config = 'config/tarefas.yaml'

	@agent
	def analista_lider_mercado(self) -> Agent:
		return Agent(
			config=self.agents_config['analista_lider_mercado'],
			tools=[search_tool, ScrapeWebsiteTool()],
			verbose=True,
			memory=False,
			llm=self.llam3_llm,
		)

	@agent
	def estrategista_chefe_marketing(self) -> Agent:
		return Agent(
			config=self.agents_config['estrategista_chefe_marketing'],
			tools=[search_tool, ScrapeWebsiteTool()],
			verbose=True,
			memory=False,
			llm=self.llam3_llm,
		)

	@agent
	def criador_conteudo_criativo(self) -> Agent:
		return Agent(
			config=self.agents_config['criador_conteudo_criativo'],
			verbose=True,
			memory=False,
			llm=self.llam3_llm,
		)

	@task
	def tarefa_pesquisa(self) -> Task:
		return Task(
			config=self.tasks_config['tarefa_pesquisa'],
			agent=self.analista_lider_mercado()
		)

	@task
	def tarefa_compreensao_projeto(self) -> Task:
		return Task(
			config=self.tasks_config['tarefa_compreensao_projeto'],
			agent=self.estrategista_chefe_marketing()
		)

	@task
	def tarefa_estrategia_marketing(self) -> Task:
		return Task(
			config=self.tasks_config['tarefa_estrategia_marketing'],
			agent=self.estrategista_chefe_marketing(),
			output_json=EstrategiaMercado
		)

	@task
	def tarefa_ideia_campanha(self) -> Task:
		return Task(
			config=self.tasks_config['tarefa_ideia_campanha'],
			agent=self.criador_conteudo_criativo(),
   		output_json=IdeiaCampanha
		)

	@task
	def tarefa_criacao_texto(self) -> Task:
		return Task(
			config=self.tasks_config['tarefa_criacao_texto'],
			agent=self.criador_conteudo_criativo(),
   		context=[self.tarefa_estrategia_marketing(), self.tarefa_ideia_campanha()],
			output_json=TextoPublicitario
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the MarketingPosts crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=2,			
		)

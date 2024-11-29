from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from .ferramentas.multiplicacao_tool import MultiplicacaoTool
from ....utils.llm_models import GEMINI_1_5_PRO

@CrewBase
class EquipeMultiplicadora():

    def __init__(self):
        self.multiplicacao_tool = MultiplicacaoTool()
        self.llm = GEMINI_1_5_PRO

    @agent
    def gerador_numeros(self) -> Agent:
        return Agent(
            config=self.agents_config['gerador_numeros'],
            llm=self.llm,
        )
    
    @agent
    def multiplicador(self) -> Agent:
        return Agent(
            config=self.agents_config['multiplicador'],
            llm=self.llm ,
        )
    
    @task
    def gerar_numeros(self) -> Task:
        return Task(
            config=self.tasks_config['gerar_numeros'],
            agent=self.gerador_numeros()
        )
    
    @task
    def multiplicar(self) -> Task:
        return Task(
            config=self.tasks_config['multiplicar'],
            tools=[self.multiplicacao_tool],
            agent=self.multiplicador()
        )

    @crew
    def equipe(self) -> Crew:
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from typing import List
from instituto_crewai.equipes.roteirizador.agente_config import AgenteConfig

@CrewBase
class EquipeExemplo():
    """
    
    """

    def __init__(self) -> None:
        """
            
        """            

    @agent
    def contador_historia(self) -> Agent:
        """
        Agentes Contador de Histórias
        """        
        return Agent(
            config=self.agents_config['contador_historia'],
            llm=LLM(model="groq/llama-3.1-70b-versatile", temperature=0.85),
            max_rpm=30,
            memory=True,
            allow_delegation=False,
            verbose=True,            
        )    
    
    
    @task
    def tarefa_contar_historia(self) -> Task: 
        """
        Tarefa contar história
        """
        return Task(
            config=self.tasks_config['tarefa_contar_historia'],
            agent=self.contador_historia(),
        )    

    @crew
    def crew(self) -> Crew:
        """
        Cria e retorna a equipe de roteiristas.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            cache=True,
            verbose=True,
            manager_llm=LLM(model="groq/llama-3.1-70b-versatile", temperature=0.65)	,
            planning=True,
            planning_llm=LLM(model="groq/llama-3.1-70b-versatile", temperature=0.25),
        )
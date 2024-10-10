from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from typing import List

@CrewBase
class EquipeAutoDoc():
    """
    
    """

    def __init__(self) -> None:
        """
            
        """            

    @agent
    def analista_processos(self) -> Agent:
        """
       
        """        
        return Agent(
            config=self.agents_config['analista_processos'],
            llm=LLM(model="groq/llama-3.2-90b-text-preview", temperature=0.25),
            max_rpm=30,
            memory=True,
            allow_delegation=False,
            verbose=True,            
        )
        
    @agent
    def especialista_documentacao(self) -> Agent:
        """
       
        """        
        return Agent(
            config=self.agents_config['especialista_documentacao'],
            llm=LLM(model="groq/llama-3.2-90b-text-preview", temperature=0.25),
            max_rpm=30,
            memory=True,
            allow_delegation=False,
            verbose=True,            
        )    
        
    # @agent
    # def auditor_documentacao(self) -> Agent:
    #     """
       
    #     """        
    #     return Agent(
    #         config=self.agents_config['auditor_documentacao'],
    #         llm=LLM(model="groq/llama-3.2-90b-text-preview", temperature=0.25),
    #         max_rpm=30,
    #         memory=True,
    #         allow_delegation=False,
    #         verbose=True,            
    #     ) 
        
    #@agent
    # def coordenador_comunicacao(self) -> Agent:
    #     """
       
    #     """        
    #     return Agent(
    #         config=self.agents_config['coordenador_comunicacao'],
    #         llm=LLM(model="groq/llama-3.2-90b-text-preview", temperature=0.25),
    #         max_rpm=30,
    #         memory=True,
    #         allow_delegation=True,
    #         verbose=True,            
    #     ) 
    
    
    @task
    def mapear_processo(self) -> Task: 
        """
       
        """
        return Task(
            config=self.tasks_config['mapear_processo'],
            agent=self.analista_processos(),
        ) 
        
    @task
    def documentar_processo(self) -> Task: 
        """
       
        """
        return Task(
            config=self.tasks_config['documentar_processo'],
            agent=self.especialista_documentacao(),
        )
        
    # @task
    # def auditar_documentacao(self) -> Task: 
    #     """
       
    #     """
    #     return Task(
    #         config=self.tasks_config['auditar_documentacao'],
    #         agent=self.auditor_documentacao(),
    #     )
        
    #@task
    def coordenar_comunicacao(self) -> Task: 
        """
       
        """
        return Task(
            config=self.tasks_config['coordenar_comunicacao'],
            agent=self.coordenador_comunicacao(),
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
            #manager_agent=self.coordenador_comunicacao(),           
            planning=True,
            planning_llm=LLM(model="groq/llama-3.1-70b-versatile", temperature=0.25),
        )
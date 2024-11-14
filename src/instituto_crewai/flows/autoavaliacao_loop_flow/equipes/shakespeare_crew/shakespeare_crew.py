from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ShakespeareCrew:

    @agent
    def agent(self) -> Agent:
        pass

    @task
    def task(self) -> Task:
        pass
    
    @crew
    def crew(self) -> Crew:
        pass

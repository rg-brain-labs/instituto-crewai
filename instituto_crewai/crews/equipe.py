from crewai import Crew, Process

class Equipe:
    def __init__(self, agents, tasks, process=Process.sequential, verbose=2, memory=True):
        self.agents = agents
        self.tasks = tasks
        self.process = process
        self.verbose = verbose
        self.memory = memory
        
    def create_crew(self):
        return Crew(
            agents = self.agents, 
            tasks = self.tasks, 
            process = self.process, 
            verbose = self.verbose, 
            memory= self.memory,
        )
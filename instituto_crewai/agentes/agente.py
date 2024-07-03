from crewai import Agent

class Agente:
    def __init__(self, role, goal, backstory, verbose, llm, tools, allow_delegation):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self.llm = llm
        self.tools = tools
        self.allow_delegation = allow_delegation

    def create_agente(self):
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=self.verbose,
            llm=self.llm,
            tools=None,
            allow_delegation=self.allow_delegation,
        )

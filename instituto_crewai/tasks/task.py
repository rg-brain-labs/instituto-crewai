from crewai import Task
from textwrap import dedent

class Task:
    def __init__(self, description, expected_output, agent, verbose=0):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.verbose = verbose

    def create_task(self):
        Task(
            description=dedent(self.description),
            expected_output=dedent(self.expected_output),
            agent=self.agent,
            verbose=self.verbose
        )

from instituto_crewai.crews.roteirista.roteirista_crew import RoteiristaCrew
from instituto_crewai.crews.roteirista.roteirista_config import default_config
from typing import Any, Dict
import sys

class RoteiristController:
    def __init__(self):
        default = default_config()
        self.agentes_config = default['agente_config']

    def roteirista_run(self, inputs: Dict[str, str]):
        """
        Run the crew.
        """
        RoteiristaCrew(self.agentes_config).crew().kickoff(inputs=inputs)

    def train(self, n_iterations: int, filename: str, inputs: Dict[str, str]):
        """
        Train the crew for a given number of iterations.
        """
        try:
            RoteiristaCrew(self.agentes_config).crew().train(n_iterations=n_iterations, filename=filename, inputs=inputs)
        except Exception as e:
            raise Exception(f"An error occurred while training the crew: {e}")

    def replay(self, task_id: str):
        """
        Replay the crew execution from a specific task.
        """
        try:
            RoteiristaCrew(self.agentes_config).crew().replay(task_id=task_id)
        except Exception as e:
            raise Exception(f"An error occurred while replaying the crew: {e}")

    def test(self, n_iterations: int, openai_model_name: str, inputs: Dict[str, str]):
        """
        Test the crew execution and returns the results.
        """
        try:
            RoteiristaCrew(self.agentes_config).crew().test(n_iterations=n_iterations, openai_model_name=openai_model_name, inputs=inputs)
        except Exception as e:
            raise Exception(f"An error occurred while testing the crew: {e}")
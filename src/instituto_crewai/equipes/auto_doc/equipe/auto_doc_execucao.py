from instituto_crewai.equipes.auto_doc.equipe.auto_doc import EquipeAutoDoc

from typing import  Dict

class AutoDocController:
    def __init__(self):       
        
        self.crew = EquipeAutoDoc().crew()

    def run(self, inputs: Dict[str, str]):
        """
        Run the crew.
        """        
        crew_result = self.crew.kickoff(inputs=inputs)
        
        return crew_result

    def train(self, n_iterations: int, filename: str, inputs: Dict[str, str]):
        """
        Train the crew for a given number of iterations.
        """
        try:
            self.crew.train(n_iterations=n_iterations, filename=filename, inputs=inputs)
        except Exception as e:
            raise Exception(f"An error occurred while training the crew: {e}")

    def replay(self, task_id: str):
        """
        Replay the crew execution from a specific task.
        """
        try:
            self.crew.replay(task_id=task_id)
        except Exception as e:
            raise Exception(f"An error occurred while replaying the crew: {e}")

    def test(self, n_iterations: int, openai_model_name: str, inputs: Dict[str, str]):
        """
        Test the crew execution and returns the results.
        """
        try:
            self.crew.test(n_iterations=n_iterations, openai_model_name=openai_model_name, inputs=inputs)
        except Exception as e:
            raise Exception(f"An error occurred while testing the crew: {e}")
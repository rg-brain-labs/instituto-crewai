from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from ....utils.llm_models import GEMINI_1_5_FLASH
import os

@CrewBase
class EquipeClassificadora():
    """
    EquipeClassificadoraCrew
    """

    def __init__(self):      
        self.llm = GEMINI_1_5_FLASH
        self.sobre_consorcio = TextFileKnowledgeSource(
            file_paths=["definicao_zenity_voyages.txt"],
        )

    @agent
    def classificador_menssagens(self) -> Agent:
        return Agent(
            config=self.agents_config["classificador_menssagens"],
            llm=self.llm,
            knowledge_sources=[self.sobre_consorcio],
            embedder={
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": os.getenv("GEMINI_API_KEY"),
                }
            }
        )

    @task
    def classificar_solicitacao(self) -> Task:
        return Task(
            config=self.tasks_config["classificar_solicitacao"],           
        )

    @crew
    def crew(self) -> Crew:
        """Cria a equipe EquipeClassificadoraCrew"""        
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # knowledge_sources=[self.sobre_consorcio],
            embedder={
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": os.getenv("GEMINI_API_KEY"),
                }
            }
        )
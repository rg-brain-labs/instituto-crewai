from typing import Optional

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel

from instituto_crewai.flows.autoavaliacao_loop_flow.ferramentas.contador_caracteres_tool import ContadorCaracteresTool

class VerificacaoPostX(BaseModel):
    validade: bool
    feedback: Optional[str]


@CrewBase
class RevisaoPostXCrew():
    """RevisaoPostXCrew"""  

    @agent
    def verificador_post_x(self) -> Agent:
        return Agent(
            config=self.agents_config["verificador_post_x"],
            tools=[ContadorCaracteresTool()],
            llm=LLM(model="groq/llama-3.2-11b-text-preview", temperature=0.70),
            memory=True,
            verbose=True,
        )

    @task
    def verificar_post_x(self) -> Task:
        return Task(
            config=self.tasks_config["verificar_post_x"],
            output_pydantic=VerificacaoPostX,
        )

    @crew
    def crew(self) -> Crew:
        """Cria a equipe RevisaoPostXCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
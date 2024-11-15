from typing import Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel

from autoavaliacao_loop_flow.ferramentas.contador_caracteres_tool import ContadorCaracteresTool

class VerificacaoPostX(BaseModel):
    valido: bool
    feedback: Optional[str]


@CrewBase
class RevisaoPostXCrew:
    """RevisaoPostXCrew"""

    configuracao_agent = "config/agents.yaml"
    configuracao_task = "config/tasks.yaml"

    @agent
    def verificador_post_x(self) -> Agent:
        return Agent(
            config=self.configuracao_agent["verificador_post_x"],
            tools=[ContadorCaracteresTool()],
        )

    @task
    def verificar_post_x(self) -> Task:
        return Task(
            config=self.configuracao_task["verificar_post_x"],
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
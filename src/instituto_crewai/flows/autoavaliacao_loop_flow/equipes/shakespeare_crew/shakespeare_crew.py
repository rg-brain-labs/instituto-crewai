from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from autoavaliacao_loop_flow.ferramentas.contador_caracteres_tool import ContadorCaracteresTool


@CrewBase
class ShakespeareCrew:
    """ShakespeareCrew"""

    configuracao_agents = "config/agents.yaml"
    configuracao_tasks = "config/tasks.yaml"

    @agent
    def bardo_shakespeariano(self) -> Agent:
        return Agent(
            config=self.configuracao_agents["bardo_shakespeariano"],
            tools=[ContadorCaracteresTool()],
        )

    @task
    def escrever_post_x(self) -> Task:
        return Task(
            config=self.configuracao_tasks["escrever_post_x"],
        )

    @crew
    def crew(self) -> Crew:
        """Cria a equipe ShakespeareCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
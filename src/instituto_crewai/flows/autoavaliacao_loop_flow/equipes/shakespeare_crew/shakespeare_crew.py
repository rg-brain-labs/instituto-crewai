from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from instituto_crewai.flows.autoavaliacao_loop_flow.ferramentas.contador_caracteres_tool import ContadorCaracteresTool

@CrewBase
class ShakespeareCrew():
    """ShakespeareCrew"""

    @agent
    def bardo_shakespeariano(self) -> Agent:
        return Agent(
            config=self.agents_config["bardo_shakespeariano"],
            tools=[ContadorCaracteresTool()],
            llm=LLM(model="groq/llama-3.2-11b-text-preview", temperature=0.25),
            memory=True,
            verbose=True,
            
        )

    @task
    def escrever_post_x(self) -> Task:
        return Task(
            config=self.tasks_config["escrever_post_x"],
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
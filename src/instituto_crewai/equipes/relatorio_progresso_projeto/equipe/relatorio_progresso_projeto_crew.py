from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from instituto_crewai.equipes.relatorio_progresso_projeto.ferramentas.extracao_dados_quadro_tool import ExtracaoDadosQuadroTool
from instituto_crewai.equipes.relatorio_progresso_projeto.ferramentas.captura_dados_cartao_tool import CapturaDadosCartaoTool

@CrewBase
class RelatorioProgressoProjetoCrew():    

  @agent
  def especialista_coleta_dados(self) -> Agent:
    return Agent(
    config=self.agents_config['especialista_coleta_dados'],
    tools=[ExtracaoDadosQuadroTool(), CapturaDadosCartaoTool()]
  )

  @agent
  def especialista_analise_projeto(self) -> Agent:
    return Agent(
    config=self.agents_config['especialista_analise_projeto']
  )

  @task
  def coletar_dados(self) -> Task:
    return Task(
    config=self.tasks_config['coletar_dados'],
    agent=self.especialista_coleta_dados()
  )

  @task
  def analisar_dados(self) -> Task:
    return Task(
    config=self.tasks_config['analisar_dados'],
    agent=self.especialista_analise_projeto(),
  )

  @task
  def gerar_relatório(self) -> Task:
    return Task(
    config=self.tasks_config['gerar_relatório'],
    agent=self.especialista_analise_projeto()
  )


  @crew
  def crew(self) -> Crew:
    return Crew(
      agents=self.agents,
      tasks=self.tasks,
      process=Process.sequential,
      verbose=True
  )

if __name__ == "__main__":  
  
 
  resultado = RelatorioProgressoProjetoCrew().crew().kickoff()

  print("RESULTADO GERAL \n\n")
  print(resultado)
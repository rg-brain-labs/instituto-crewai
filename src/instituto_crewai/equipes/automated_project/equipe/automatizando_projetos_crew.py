# poetry run .\src\instituto_crewai\equipes\automated_project\equipe\automated_project_crew.py
from typing import List
from pydantic import BaseModel, Field
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

class EstimacaoTarefa(BaseModel):
    nome_tarefa: str = Field(..., description="Nome da tarefa")
    tempo_estimado_horas: float = Field(..., description="Tempo estimado para conclusão da tarefa em horas")
    recursos_necessarios: List[str] = Field(..., description="Lista de recursos necessários para concluir a tarefa")

class Marco(BaseModel):
    nome_marco: str = Field(..., description="Nome do marco")
    tarefas: List[str] = Field(..., description="Lista de IDs de tarefas associadas a este marco")

class PlanoProjeto(BaseModel):
    tarefas: List[EstimacaoTarefa] = Field(..., description="Lista de tarefas com suas estimativas")
    marcos: List[Marco] = Field(..., description="Lista de marcos do projeto")

@CrewBase
class AutomatizandoProjetosCrew():    

  @agent
  def planejador_projeto(self) -> Agent:
    return Agent(
    config=self.agents_config['planejador_projeto']
  )

  @agent
  def analista_estimativas(self) -> Agent:
    return Agent(
    config=self.agents_config['analista_estimativas']
  )

  @agent
  def estrategista_alocacao_recursos(self) -> Agent:
    return Agent(
    config=self.agents_config['estrategista_alocacao_recursos']
  )

  @task
  def desmembra_projeto(self) -> Task:
    return Task(
    config=self.tasks_config['desmembra_projeto'],
    agent=self.planejador_projeto()
  )

  @task
  def estimar_tempo_recurso(self) -> Task:
    return Task(
    config=self.tasks_config['estimar_tempo_recurso'],
    agent=self.analista_estimativas()
  )

  @task
  def alocar_recursos(self) -> Task:
    return Task(
    config=self.tasks_config['alocar_recursos'],
    agent=self.estrategista_alocacao_recursos(),
    output_pydantic=PlanoProjeto
  )

  @crew
  def crew(self) -> Crew:
    return Crew(
      agents=self.agents,
      tasks=self.tasks,
      process=Process.sequential,
      verbose=True
  )

# if __name__ == "__main__":
  
#   projeto = 'Website'
#   industria = 'Tecnologia'
#   objetivos_projeto = 'Criar um website para uma pequena empresa'
#   membros_equipe = """
#   - John Doe (Gerente de Projeto)
#   - Jane Doe (Engenheira de Software)
#   - Bob Smith (Designer)
#   - Alice Johnson (Engenheira de QA)
#   - Tom Brown (Engenheira de QA)
#   """
#   requisitos_projeto = """
#   - Criar um design responsivo que funcione bem em dispositivos desktop e móveis
#   - Implementar uma interface de usuário moderna e visualmente atraente com um visual limpo
#   - Desenvolver um sistema de navegação amigável com uma estrutura de menu intuitiva
#   - Incluir uma página "Sobre Nós" destacando a história e os valores da empresa
#   - Projetar uma página "Serviços" exibindo as ofertas da empresa com descrições
#   - Criar uma página "Contato" com um formulário e mapa integrado para comunicação
#   - Implementar uma seção de blog para compartilhar notícias do setor e atualizações da empresa
#   - Garantir tempos de carregamento rápidos e otimizar para mecanismos de busca (SEO)
#   - Integrar links de mídia social e capacidades de compartilhamento
#   - Incluir uma seção de depoimentos para exibir o feedback dos clientes e construir confiança
#   """

#   inputs = {
#     'tipo_projeto': projeto,
#     'objetivos_projeto': objetivos_projeto,
#     'industria': industria,
#     'membros_equipe': membros_equipe,
#     'requisitos_projeto': requisitos_projeto
#   }
 
#   result = AutomatizandoProjetosCrew().crew().kickoff(
#     inputs=inputs
#   )  

#   result.pydantic.dict()
#   tasks = result.pydantic.dict()['tarefas']
#   milestones = result.pydantic.dict()['marcos']

#   print("RESULTADO GERAL \n\n")
#   print(result)

#   print("\n\n TAREFAS \n\n")
#   print(tasks)

#   print("\n\n MILESTONES \n\n")
#   print(milestones)

   # import pandas as pd

  # costs = 0.150 * (crew.usage_metrics.prompt_tokens + crew.usage_metrics.completion_tokens) / 1_000_000
  # print(f"Total costs: ${costs:.4f}")

  # # Convert UsageMetrics instance to a DataFrame
  # df_usage_metrics = pd.DataFrame([crew.usage_metrics.dict()])
  # df_usage_metrics
  
  # df_tasks = pd.DataFrame(tasks)

  # Display the DataFrame as an HTML table
  # df_tasks.style.set_table_attributes('border="1"').set_caption("Task Details").set_table_styles(
  #     [{'selector': 'th, td', 'props': [('font-size', '120%')]}]
  # )
  # df_milestones = pd.DataFrame(milestones)

  # # Display the DataFrame as an HTML table
  # df_milestones.style.set_table_attributes('border="1"').set_caption("Task Details").set_table_styles(
  #     [{'selector': 'th, td', 'props': [('font-size', '120%')]}]
  # )
import os
from crewai import Agent, Task, Crew, Process

# Agente Analista de Estrutura
analista_estrutura = Agent(
    role='Analista de Estrutura',
    goal='Avaliar a estrutura narrativa do roteiro.',
    verbose=True,
    memory=True,
    backstory=(
        "Você é especialista em narrativa, com um olhar afiado para a estrutura de histórias. Sua missão é garantir que todos os elementos narrativos estejam presentes e bem desenvolvidos."
    ),
    tools=[]
)

# Agente Analista de Personagens
analista_personagens = Agent(
    role='Analista de Personagens',
    goal='Avaliar a profundidade e a coerência dos personagens no roteiro.',
    verbose=True,
    memory=True,
    backstory=(
        "Você é um profundo conhecedor da psicologia dos personagens, capaz de identificar a coerência em suas ações, diálogos e desenvolvimento ao longo da história."
    ),
    tools=[]
)

# Agente Analista de Coerência e Originalidade
analista_coerencia_originalidade = Agent(
    role='Analista de Coerência e Originalidade',
    goal='Avaliar a coerência do enredo e a originalidade da história.',
    verbose=True,
    memory=True,
    backstory=(
        "Você é um crítico rigoroso, sempre atento a clichês e inconsistências. Sua tarefa é garantir que a história seja única e coerente do início ao fim."
    ),
    tools=[]
)

# Definição das tarefas

# Tarefa 1: Análise da Estrutura Narrativa
tarefa_analise_estrutura = Task(
    description=(
        "Avalie a estrutura do roteiro, verificando a presença e a qualidade dos seguintes elementos: Conflito Inicial, Desenvolvimento, Clímax, Resolução e Conclusão."
    ),
    expected_output='Relatório detalhado sobre a estrutura narrativa do roteiro.',
    tools=[],
    agent=analista_estrutura,
)

# Tarefa 2: Análise de Personagens
tarefa_analise_personagens = Task(
    description=(
        "Examine os personagens do roteiro, avaliando sua profundidade, motivações, e coerência ao longo da narrativa."
    ),
    expected_output='Relatório detalhado sobre o desenvolvimento e a coerência dos personagens.',
    tools=[],
    agent=analista_personagens,
)

# Tarefa 3: Análise de Coerência e Originalidade
tarefa_analise_coerencia_originalidade = Task(
    description=(
        "Avalie a coerência do enredo e a originalidade da história, identificando possíveis clichês ou inconsistências."
    ),
    expected_output='Relatório detalhado sobre a coerência e originalidade do roteiro.',
    tools=[],
    agent=analista_coerencia_originalidade,
)

# Tarefa 4: Classificação Final do Roteiro
tarefa_classificacao_final = Task(
    description=(
        "Com base nas análises anteriores, classifique o roteiro em termos de qualidade narrativa, desenvolvimento de personagens e originalidade."
    ),
    expected_output='Classificação final do roteiro com base nos critérios estabelecidos.',
    tools=[],
    agent=[analista_estrutura, analista_personagens, analista_coerencia_originalidade],
)

# Formação da equipe
equipe_analise_roteiros = Crew(
    agents=[analista_estrutura, analista_personagens, analista_coerencia_originalidade],
    tasks=[tarefa_analise_estrutura, tarefa_analise_personagens, tarefa_analise_coerencia_originalidade, tarefa_classificacao_final],
    process=Process.parallel  # Análises são feitas em paralelo
)

# Iniciar o processo de análise e classificação do roteiro
resultado = equipe_analise_roteiros.kickoff(inputs={'roteiro': 'Seu roteiro aqui'})
print(resultado)

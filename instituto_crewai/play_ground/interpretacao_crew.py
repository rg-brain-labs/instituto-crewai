import os
from crewai import Agent, Task, Crew, Process

# Personagem A
personagem_a = Agent(
    role='Personagem A',
    goal='Interprete suas falas e emoções no diálogo com o Personagem B.',
    verbose=True,
    memory=True,
    backstory=(
        "Você é o protagonista desta cena, trazendo profundidade emocional e intensidade às suas falas."
    ),
    tools=[]
)

# Personagem B
personagem_b = Agent(
    role='Personagem B',
    goal='Interprete suas falas e emoções no diálogo com o Personagem A.',
    verbose=True,
    memory=True,
    backstory=(
        "Você é o antagonista desta cena, com uma perspectiva forte e desafiadora."
    ),
    tools=[]
)

# Tarefa 1: Leitura e Compreensão do Roteiro
tarefa_compreensao_roteiro = Task(
    description=(
        "Leia e compreenda o roteiro, identificando suas falas, sentimentos e o contexto da narrativa. Prepare-se para interpretar seu personagem."
    ),
    expected_output='Falas e emoções dos personagens compreendidas e prontas para a interpretação.',
    tools=[],
    agent=[personagem_a, personagem_b],
)

# Tarefa 2: Geração do Diálogo
tarefa_geracao_dialogo = Task(
    description=(
        "Gere o diálogo entre os dois personagens, seguindo o roteiro e expressando as emoções indicadas."
    ),
    expected_output='Diálogo gerado entre os personagens, incluindo emoções e entonações.',
    tools=[],
    agent=[personagem_a, personagem_b],
)

# Formação da equipe
equipe_interpretacao = Crew(
    agents=[personagem_a, personagem_b],
    tasks=[tarefa_compreensao_roteiro, tarefa_geracao_dialogo],
    process=Process.sequential
)

# Iniciar o processo de interpretação do roteiro
resultado = equipe_interpretacao.kickoff(inputs={'roteiro': 'Seu roteiro aqui'})
print(resultado)

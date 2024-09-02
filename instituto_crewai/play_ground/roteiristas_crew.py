import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

# Configuração das chaves de API 
dotenv_path = Path(__file__).parents[1] / 'config' / '.env'
load_dotenv(dotenv_path)

# LLMs Dos Agentes
gemini = ChatGoogleGenerativeAI(
            model='gemini-1.5-flash',
            verbose=True,
            temperature=0.5,
        )
gemini_max_rpm = 15

llama = ChatGroq(
            model='llama-3.1-8b-instant',
            verbose=True,
            temperature=0.5,
        )
max_rpm = 30

# Ferramentas para busca e análise de informações
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

#Agentes

# Agente responsável por analisar o texto base
analista_de_texto = Agent(
    role='Analista de Texto',
    goal='Analisar o texto base e extrair os principais pontos de conflito para criar um roteiro.',
    backstory=(
        "Você é um analista experiente, capaz de identificar nuances e conflitos em qualquer texto, "
        "transformando informações brutas em um esqueleto de roteiro."
    ),
    verbose=True,
    memory=True,
    llm=gemini,
    max_rpm=gemini_max_rpm,
)

# # Roteirista principal
# roteirista_principal = Agent(
#     role='Roteirista Principal',
#     goal='Criar o esqueleto de um roteiro a partir de um texto base analisado.',
#     backstory=(
#         "Você é um roteirista talentoso, com a habilidade de estruturar uma narrativa envolvente a partir de qualquer informação fornecida."
#     ),   
#     verbose=True,
#     memory=True,
#     llm=llama,
#     max_rpm=max_rpm
# )

# # Agente responsável pelos diálogos
# dialogista = Agent(
#     role='Dialogista',
#     goal='Desenvolver diálogos detalhados e emocionalmente ricos para o roteiro.',
#     backstory=(
#         "Você é especialista em criar diálogos autênticos e emocionantes que capturam a essência dos personagens e a tensão da narrativa."
#     ),   
#     verbose=True,
#     memory=True,
#     llm=llama,
#     max_rpm=max_rpm
# )

# # Revisor do roteiro
# revisor_de_roteiro = Agent(
#     role='Revisor de Roteiro',
#     goal='Revisar o roteiro e garantir a coesão e consistência da narrativa.',
#     backstory=(
#         "Você é um crítico detalhista, com um olhar afiado para erros e inconsistências, garantindo que o roteiro final seja impecável."
#     ),   
#     verbose=True,
#     memory=True,
#     llm=llama,
#     max_rpm=max_rpm
# )

# # Definição das tarefas

# Tarefa 1: Análise do Texto Base
tarefa_analise_texto = Task(
    description=(
        "Analise o texto base fornecido e extraia os principais pontos de conflito e temas. "
        "Identifique as informações cruciais que servirão de base para o desenvolvimento do roteiro."

        "{texto_base}"
    ),
    expected_output='Lista de pontos de conflito e temas extraídos do texto base.',
    tools=[search_tool, scrape_tool],
    agent=analista_de_texto,
)

# # Tarefa 2: Criação do Esqueleto do Roteiro
# tarefa_criacao_roteiro = Task(
#     description=(
#         "Com base na análise do texto base, crie o esqueleto de um roteiro, organizando os principais pontos da história em: Conflito Inicial, "
#         "Desenvolvimento, Clímax, Resolução e Conclusão."
#     ),
#     expected_output='Esqueleto do roteiro organizado nos principais pontos narrativos.',   
#     agent=roteirista_principal,
# )

# # Tarefa 3: Desenvolvimento dos Diálogos
# tarefa_desenvolvimento_dialogos = Task(
#     description=(
#         "Expanda o esqueleto do roteiro com diálogos detalhados entre os personagens. Adicione nuances emocionais e garanta que os sentimentos expressos "
#         "estejam alinhados com a narrativa e o estilo proposto."
#     ),
#     expected_output='Roteiro completo com diálogos detalhados, incluindo as emoções dos personagens em cada fala.',    
#     agent=dialogista,
# )

# # Tarefa 4: Revisão e Ajustes Finais
# tarefa_revisao_roteiro = Task(
#     description=(
#         "Revisar o roteiro completo para garantir coesão, consistência e fidelidade ao texto base. Faça ajustes necessários para que o roteiro final esteja "
#         "impecável e adequado ao estilo proposto."
#     ),
#     expected_output='Roteiro final revisado e ajustado.',    
#     agent=revisor_de_roteiro,
# )

# Formação da equipe
equipe_roteiristas = Crew(
    agents=[
        analista_de_texto, 
        #roteirista_principal, dialogista, revisor_de_roteiro
    ],
    tasks=[
        tarefa_analise_texto, 
        #tarefa_criacao_roteiro, tarefa_desenvolvimento_dialogos, tarefa_revisao_roteiro
    ],
    process=Process.sequential
)

texto_base = """
Thaís Carla processa Danilo Gentili por gordofobia.

A dançarina e influenciadora digital Thaís Carla entrou com um processo judicial contra o 
apresentador Danilo Gentili no Tribunal de Justiça da Bahia (TJ-BA), acusando-o de praticar 
gordofobia. O apresentador do programa The Noite, do SBT, já havia sido processado por Thaís 
anteriormente pelo mesmo motivo.

Desta vez, a influenciadora está solicitando uma retratação pública nas redes sociais de 
Gentili, além de uma indenização no valor de R$ 15 mil. Segundo informações dos portais F5, 
da Folha de S.Paulo, e Metrópoles, Thaís acusa o apresentador de fazer comentários depreciativos 
sobre sua aparência física, o que, segundo ela, fomenta ataques contra sua pessoa.

Desde 2019, Thaís Carla alega ser alvo de comentários ofensivos de Gentili, que foi obrigado, 
há dois anos, a apagar imagens dela após uma decisão judicial. No último dia 27, foi feita uma 
tentativa de acordo para evitar o processo judicial, mas sem sucesso. Ainda não há previsão 
para o julgamento, mas a influenciadora espera que a situação seja resolvida rapidamente.

Thaís Carla é uma figura conhecida na mídia por defender os direitos das pessoas gordas e 
ganhou destaque ao aparecer no programa Domingão do Faustão, da TV Globo, no final dos anos 
2010. Ela também integrou o balé da cantora Anitta entre 2017 e 2019, além de participar de 
diversos outros programas de televisão.
"""

# Iniciar o processo de criação do roteiro
resultado = equipe_roteiristas.kickoff(inputs={'texto_base': texto_base})

print(resultado)

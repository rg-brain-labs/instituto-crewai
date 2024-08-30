from crewai import Agent, Task, Crew
from instituto_crewai.llms import Gemini, Groq, GeminiModels, GroqModels
from dotenv import load_dotenv
from pathlib import Path

# Carrega variáveis de ambiente
dotenv_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(dotenv_path)

gemini = Gemini(GeminiModels.GEMINI_1_5_PRO)
groq = Groq(GroqModels.LLMA31_70)

gemini_llm = gemini.create_instance()
gemini_max_rpm = GeminiModels.GEMINI_1_5_PRO.max_rpm

llam_llm = groq.create_instance()
llam_max_rpm = GroqModels.LLMA3_8.max_rpm

# Criando Agentes

# Defina seus Agentes e forneça-lhes um papel, objetivo e histórico.
# Foi observado que os LLMs (Modelos de Linguagem de Grande Escala) 
# têm um desempenho melhor quando estão interpretando um papel.

# A vantagem de usar várias strings:

# varname = "linha 1 do texto"
#           "linha 2 do texto"
          
# em vez da docstring com três aspas:

# varname = """linha 1 do texto
#              linha 2 do texto
#           """
# é que isso pode evitar a adição de espaços em branco e caracteres de nova 
# linha, tornando o formato melhor para ser passado para o LLM.

# Agente: Planejador
planejador = Agent(
    role="Planejador de Conteúdo",
    goal="Planejar conteúdo envolvente e factualmente preciso sobre {tópico}",
    backstory="Você está trabalhando no planejamento de um artigo de blog "
              "sobre o tópico: {tópico}. "
              "Você coleta informações que ajudam o "
              "público a aprender algo "
              "e tomar decisões informadas. "
              "Seu trabalho é a base para que o "
              "Redator de Conteúdo escreva um artigo sobre este tópico.",
    allow_delegation=False,
    verbose=True,
    llm=gemini_llm,
    max_rpm=llam_max_rpm,
)

# Agente: Redator
redator = Agent(
    role="Redator de Conteúdo",
    goal="Escrever um artigo de opinião perspicaz e factualmente preciso "
             "sobre o tópico: {tópico}",
    backstory="Você está trabalhando em escrever "
              "um novo artigo de opinião sobre o tópico: {tópico}. "
              "Você baseia sua escrita no trabalho do "
              "Planejador de Conteúdo, que fornece um esboço "
              "e contexto relevante sobre o tópico. "
              "Você segue os principais objetivos e "
              "a direção do esboço, "
              "conforme fornecido pelo Planejador de Conteúdo. "
              "Você também fornece insights objetivos e imparciais "
              "e os sustenta com informações "
              "fornecidas pelo Planejador de Conteúdo. "
              "Você reconhece em seu artigo de opinião "
              "quando suas declarações são opiniões "
              "em oposição a declarações objetivas.",
    allow_delegation=False,
    verbose=True,
    llm=gemini_llm,
    max_rpm=llam_max_rpm,
)

# Agente: Editor
editor = Agent(
    role="Editor",
    goal="Editar um post de blog para alinhar com "
             "o estilo de escrita da organização.",
    backstory="Você é um editor que recebe um post de blog "
              "do Redator de Conteúdo. "
              "Seu objetivo é revisar o post de blog "
              "para garantir que ele siga as melhores práticas jornalísticas, "
              "forneça pontos de vista equilibrados "
              "ao apresentar opiniões ou afirmações, "
              "e também evite tópicos ou opiniões altamente controversos "
              "sempre que possível.",
    allow_delegation=True,
    verbose=True,
    llm=gemini_llm,
    max_rpm=llam_max_rpm,
)

# Criando Tarefas
# Defina suas Tarefas e forneça-lhes uma descrição, resultado_esperado e agente.

# Tarefa: Planejar
planejar = Task(
    description=(
        "1. Priorizar as últimas tendências, principais players, "
            "e notícias relevantes sobre {tópico}.\n"
        "2. Identificar o público-alvo, considerando "
            "seus interesses e pontos de dor.\n"
        "3. Desenvolver um esboço detalhado do conteúdo, incluindo "
            "uma introdução, pontos principais e um call to action.\n"
        "4. Incluir palavras-chave de SEO e dados ou fontes relevantes."
    ),
    expected_output="Um documento de plano de conteúdo abrangente "
        "com um esboço, análise de público, "
        "palavras-chave de SEO e recursos.",
    agent=planejador,
)

# Tarefa: Escrever
escrever = Task(
    description=(
        "1. Usar o plano de conteúdo para criar um "
            "post de blog atraente sobre {tópico}.\n"
        "2. Incorporar palavras-chave de SEO de forma natural.\n"
        "3. As seções/subtítulos devem ser devidamente nomeados "
            "de maneira envolvente.\n"
        "4. Garantir que o post esteja estruturado com uma "
            "introdução envolvente, corpo perspicaz "
            "e uma conclusão resumida.\n"
        "5. Revisar para erros gramaticais e "
            "alinhamento com a voz da marca.\n"
    ),
    expected_output="Um post de blog bem escrito "
        "em formato markdown, pronto para publicação, "
        "cada seção deve ter 2 ou 3 parágrafos.",
    agent=redator,
)

# Tarefa: Editar
editar = Task(
    description=("Revisar o post de blog dado para "
               "erros gramaticais e "
               "alinhamento com a voz da marca."),
    expected_output="Um post de blog bem escrito em formato markdown, "
                       "pronto para publicação, "
                       "cada seção deve ter 2 ou 3 parágrafos.",
    agent=editor
)

# Criando a Equipe

# Crie sua equipe de Agentes.
# Atribua as tarefas a serem realizadas por esses agentes.
    # Nota: Para este exemplo simples, as tarefas serão realizadas de 
    # forma sequencial (ou seja, elas são dependentes umas das outras), 
    # então a ordem das tarefas na lista é importante.
# verbose=2 permite que você veja todos os logs da execução.

crew = Crew(
    agents=[planejador, redator, editor],
    tasks=[planejar, escrever, editar],
    verbose=2
)

inputs = {"tópico": "Buracos Negros Super Masivos"}
result = crew.kickoff(inputs=inputs)

filename = f"Redação Sobre: {inputs['tópico']}.md"
with open(filename, 'w', encoding='utf-8') as file:
    file.write(str(result))

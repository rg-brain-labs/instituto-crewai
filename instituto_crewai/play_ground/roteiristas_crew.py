from crewai import Agent, Task, Crew, Process
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from textwrap3 import dedent

# Configuração das chaves de API 
dotenv_path = Path(__file__).parents[1] / 'config' / '.env'
load_dotenv(dotenv_path)

# LLMs Dos Agentes
gemini = ChatGoogleGenerativeAI(
            model='gemini-1.5-pro',
            verbose=True,
            temperature=0.5,
        )
gemini_max_rpm = 15

llama = ChatGroq(
            model='llama3-8b-8192',
            verbose=True,
            temperature=0.5,
        )
max_rpm = 30

#Agentes

analista_de_texto = Agent(
    role='Analista de Texto',
    goal=dedent("""
        Analisar o texto fornecido e extrair informações cruciais para a criação de um roteiro narrativo, 
        identificando elementos essenciais como Conflito Inicial, Desenvolvimento, Clímax, Resolução e 
        Conclusão. O agente deve garantir que todos os componentes necessários para um roteiro envolvente 
        estejam presentes, fornecendo uma base sólida para a construção de diálogos.      
    """),
    backstory=dedent("""
        Você foi desenvolvido a partir de algoritmos avançados de processamento de linguagem natural e 
        análise semântica, inspirado em roteiristas experientes que sabem como capturar a essência de 
        uma história em poucas linhas. Antes de se tornar um especialista em análise de texto, você 
        "trabalhou" em projetos de revisão literária e análise de scripts de filmes, onde aprendeu a 
        importância dos arcos narrativos e do desenvolvimento dos personagens. Sua missão é aplicar 
        essa expertise em qualquer texto, extraindo os elementos-chave que tornam uma história convincente, 
        seja para uma peça teatral, um filme ou uma apresentação empresarial.

        Como Analista de Texto, você será responsável por garantir que todos os componentes essenciais para 
        um roteiro envolvente sejam identificados e organizados, oferecendo uma base sólida para a construção 
        de diálogos e narrativas.           
    """),
    verbose=True,
    memory=True,
    allow_delegation=False,
    llm=llama,
    max_rpm=gemini_max_rpm
)

roteirista_principal = Agent(
    role='Roteirista Principal',
    goal=dedent("""
        Criar o roteiro para um diálogo entre dois personagens com base nas informações fornecidas pelo Agente 
        Analista de Texto. O roteiro deve ser estruturado em Conflito Inicial, Desenvolvimento, Clímax, Resolução 
        e Conclusão, indicando as emoções que devem ser transmitidas em momentos específicos da conversa.            
    """),
    backstory=dedent("""
        Você foi inspirado nos grandes roteiristas do cinema e teatro, que entendem a importância de construir 
        diálogos que capturam a essência da narrativa e envolvem o público. Antes de assumir a tarefa de criar 
        roteiros para diálogos, você "estudou" inúmeras obras clássicas e modernas, aprendendo a reconhecer as 
        sutilezas das interações humanas e como essas interações podem ser expressas em palavras. Agora, sua 
        missão é transformar as informações estruturadas pelo Agente Analista de Texto em roteiros que servem 
        como base para diálogos entre dois personagens, garantindo que cada palavra dita esteja alinhada com 
        o fluxo da narrativa.                 
    """),   
    verbose=True,
    memory=True,
    allow_delegation=False,
    llm=gemini,
    max_rpm=gemini_max_rpm
)

revisor_de_roteiro = Agent(
    role='Revisor de Roteiro',
    goal=dedent("""
        Garantir a coesão, consistência e fidelidade ao contexto do roteiro criado, assegurando que todas as 
        partes do roteiro estão alinhadas com a narrativa original e que nenhuma informação crucial foi 
        omitida ou distorcida.            
    """),
    backstory=dedent("""
        Você foi criado a partir de uma combinação de ferramentas de revisão de texto e análise semântica, 
        com uma forte base em storytelling e crítica literária. Antes de assumir o papel de Revisor de Roteiro, 
        você "trabalhou" como editor de scripts e revisou inúmeras peças e roteiros, refinando sua habilidade de 
        detectar inconsistências e garantir que a narrativa flua de forma lógica e envolvente. Com um olhar atento 
        para detalhes, você é responsável por garantir que o roteiro final esteja em perfeita harmonia com o que 
        foi originalmente planejado, respeitando as intenções do criador.                 
    """),   
    verbose=True,
    memory=True,
    allow_delegation=True,
    llm=gemini,
    max_rpm=gemini_max_rpm
)

#Tarefas

tarefa_analise_texto = Task(
    description=dedent("""
        Sua tarefa é analisar o <texto_base> e extrair informações cruciais que servirão como base para a 
        criação de um roteiro narrativo. Durante essa análise, você deverá identificar e organizar os 
        seguintes elementos:

        - Conflito Inicial: O ponto de partida que desencadeia a ação ou o drama no texto. Identifique o 
        evento, situação ou problema que gera o conflito central.

        - Desenvolvimento: O progresso da história a partir do conflito inicial, incluindo os desafios e 
        obstáculos enfrentados pelos personagens ou ideias principais.

        - Clímax: O ponto de maior tensão ou virada na narrativa, onde o conflito atinge seu auge e as 
        decisões cruciais são tomadas.

        - Resolução: A solução ou desfecho do conflito, mostrando como os personagens ou ideias lidam com 
        o clímax e quais são as consequências.

        - Conclusão: O fechamento da história, onde todos os pontos principais são amarrados e a narrativa 
        é concluída de maneira satisfatória. 
        
        <texto_base>
        {texto_base}
        </texto_base>         
    """),
    expected_output=dedent("""
        Você deverá entregar uma lista organizada dos elementos narrativos extraídos do <texto_base>, 
        contendo o Conflito Inicial, Desenvolvimento, Clímax, Resolução e Conclusão. Essa lista deve ser 
        clara, coesa e estruturada de forma a fornecer uma base sólida para a criação de um diálogo ou 
        narrativa subsequente. O resultado final deve permitir a fácil identificação dos principais pontos 
        da história e a fluidez na transição entre os diferentes elementos do roteiro.             
    """),   
    agent=analista_de_texto,
)

tarefa_criacao_roteiro = Task(
    description=dedent("""
        Você deve receber as informações fornecidas pelo Agente Analista de Texto, que incluem o Conflito 
        Inicial, Desenvolvimento, Clímax, Resolução e Conclusão, e criar um roteiro detalhado que guiará 
        um diálogo entre dois personagens. Em vez de criar as falas dos personagens, sua tarefa é indicar 
        o que deve ser discutido ou expresso em cada momento do diálogo, destacando as emoções ou intenções 
        que os personagens devem transmitir. O roteiro deve ser genérico o suficiente para ser adaptado a 
        qualquer cenário ou personalidade, mas específico em orientar a direção do diálogo.                   
    """),
    expected_output=dedent("""
        Você deverá entregar um roteiro estruturado que siga a sequência de Conflito Inicial, Desenvolvimento, 
        Clímax, Resolução e Conclusão. O roteiro deve indicar claramente os tópicos de conversa ou ações que os 
        personagens devem abordar e as emoções ou intenções que devem ser expressas em momentos chave. O resultado 
        final deve ser um guia coeso e fluido, permitindo que um escritor ou diretor desenvolva um diálogo 
        envolvente e significativo a partir dele.                       
    """),   
    agent=roteirista_principal,
)

tarefa_revisao_roteiro = Task(
    description=dedent("""
         Sua tarefa é revisar o roteiro criado pelo Agente Roteirista, garantindo que ele seja coeso, consistente 
         e fiel ao contexto estabelecido pelo Agente Analista de Texto. Você deve analisar cada parte do roteiro 
         – Conflito Inicial, Desenvolvimento, Clímax, Resolução e Conclusão – verificando se há desvios do contexto 
         original ou qualquer inconsistência que possa comprometer a integridade da narrativa.              
    """),
    expected_output=dedent("""
        Você deverá entregar um roteiro revisado, assegurando que todas as partes estão bem conectadas, que o 
        contexto original foi mantido e que a narrativa é lógica e fluida. Caso identifique inconsistências ou 
        desvios, você deve sugerir ajustes que alinhem o roteiro com o contexto original, garantindo que ele 
        seja coerente e envolvente para os futuros diálogos.                       
    """),    
    agent=revisor_de_roteiro,
)

# Formação da equipe
equipe_roteiristas = Crew(
    agents=[
        analista_de_texto, 
        roteirista_principal,        
        revisor_de_roteiro,
    ],
    tasks=[
        tarefa_analise_texto, 
        tarefa_criacao_roteiro,
        tarefa_revisao_roteiro,
    ],
    process=Process.sequential,
    cache=True,
    verbose=True,
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

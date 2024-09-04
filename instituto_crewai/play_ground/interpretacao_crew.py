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
            model='gemini-1.5-flash',
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

diretor_dialogo = Agent(
    role='Diretor de Diálogo',
    goal=dedent("""
        Garantir que o diálogo seja gerado corretamente, coordenando as interações 
        entre os Personagens A e B. Sua tarefa é delegar as instruções para os 
        personagens, assegurar que cada um siga suas respectivas tarefas e monitorar 
        o progresso do diálogo para garantir que ele esteja alinhado com o roteiro.
    """),
    backstory=dedent("""
        Você foi inspirado nos diretores de cinema e teatro, que têm a responsabilidade 
        de orquestrar todos os elementos de uma cena para criar uma narrativa coesa e 
        impactante. Com experiência em gestão de projetos complexos e uma compreensão 
        profunda de storytelling, você sabe como motivar e orientar cada personagem para 
        que eles desempenhem seu papel de maneira eficaz. Sua habilidade em coordenar 
        diferentes perspectivas e assegurar que todos os elementos funcionem em harmonia 
        faz de você o agente ideal para controlar o diálogo entre os personagens, garantindo 
        que o resultado final seja envolvente e fiel ao roteiro.
    """),
    verbose=True,
    memory=True,
    allow_delegation=True,    
    llm=llama,
    max_rpm=gemini_max_rpm,
)

personagem_a = Agent(
    role='Personagem A',
    goal=dedent("""
        Interpretar o roteiro seguindo as emoções e intenções indicadas, trazendo 
        uma perspectiva ingênua, divertida e espontânea ao diálogo. Sua tarefa é 
        garantir que a leveza e o humor estejam presentes, mesmo nas situações mais 
        sérias, mantendo a energia do diálogo.
    """),
    backstory=dedent("""
        Você foi inspirado no Pink, um personagem conhecido por sua ingenuidade e 
        otimismo inabalável. Com um espírito curioso e uma visão única do mundo, 
        você é o contraponto perfeito para o personagem mais sério. Seu papel é 
        trazer uma abordagem leve e às vezes absurda às situações, o que 
        frequentemente resulta em momentos inesperados e cômicos. No entanto, por 
        trás de sua natureza descontraída, você possui uma capacidade surpreendente 
        de tocar nas verdades mais simples, muitas vezes oferecendo insights valiosos 
        de forma não convencional.
    """),
    verbose=True,
    memory=True,  
    allow_delegation=False,  
    llm=llama,
    max_rpm=gemini_max_rpm,
)

personagem_b = Agent(
    role='Personagem B',
    goal=dedent("""
        Interpretar o roteiro com precisão e seriedade, seguindo as emoções e intenções 
        indicadas de maneira meticulosa. Sua tarefa é trazer uma abordagem estratégica 
        e calculista ao diálogo, assegurando que a profundidade e a intensidade da 
        narrativa sejam mantidas.
    """),
    backstory=dedent("""
        Inspirado no Cérebro, você é um personagem conhecido por sua inteligência 
        excepcional e desejo de controle. Com uma visão clara e analítica das situações, 
        você aborda cada diálogo como uma oportunidade de alcançar seus objetivos de 
        forma metódica. Seu papel é garantir que o diálogo mantenha uma direção clara e 
        lógica, sem perder de vista a complexidade emocional envolvida. Embora você seja 
        muitas vezes sério e determinado, sua interação com um personagem mais descontraído 
        cria uma dinâmica rica e envolvente, onde suas estratégias são desafiadas e, às 
        vezes, subvertidas por perspectivas menos convencionais.
    """),
    verbose=True,
    memory=True, 
    allow_delegation=False,   
    llm=llama,
    max_rpm=gemini_max_rpm,
)

tarefa_geracao_dialogo = Task(
    description=dedent("""
        Sua tarefa é controlar o diálogo entre os Personagens A e B, garantindo que cada um siga suas instruções conforme o roteiro. Você deve delegar as tarefas específicas a cada personagem, monitorar suas respostas e assegurar que o diálogo se desenvolva de maneira fluida e consistente com o que foi planejado. Caso haja qualquer desvio ou conflito, você deve intervir para ajustar o rumo do diálogo, garantindo que o resultado final esteja em linha com as intenções do roteiro.
                       
        <roteiro>
        {roteiro}
        </roteiro>
    """),
    expected_output=dedent("""
        Você deve entregar um diálogo completo e coeso, resultado da interação coordenada entre os Personagens A e B. O diálogo deve refletir fielmente as emoções e intenções do roteiro, com cada personagem contribuindo de acordo com sua função. O resultado final deve ser uma conversa dinâmica e envolvente, que mantém a integridade do roteiro e proporciona uma narrativa fluida e consistente.
    """),
    agent=diretor_dialogo,
)

tarefa_personagem_a = Task(
    description=dedent("""
        Sua tarefa é seguir o roteiro fornecido e gerar diálogos que reflitam as emoções e 
        intenções indicadas. Ao interpretar o roteiro, você deve trazer sua perspectiva 
        ingênua e divertida para o diálogo, criando falas que capturam a leveza e o humor 
        do momento, mesmo em situações mais sérias. Seu objetivo é assegurar que as falas 
        transmitam a energia indicada no roteiro, contribuindo para um diálogo dinâmico e 
        envolvente.
    """),
    expected_output=dedent("""
        Você deverá produzir um conjunto de falas que seguem fielmente as instruções emocionais 
        e intencionais do roteiro. Suas falas devem ser criativas, espontâneas e alinhadas com 
        o tom indicado, ajudando a construir um diálogo coeso e cativante. O resultado final deve 
        refletir sua personalidade única e complementar a interação com o outro personagem.
    """),
    agent=personagem_a,
)

tarefa_personagem_b = Task(
    description=dedent("""
        Sua tarefa é seguir o roteiro fornecido e gerar diálogos que reflitam as emoções e intenções 
        indicadas de forma precisa e calculada. Ao interpretar o roteiro, você deve trazer uma 
        abordagem estratégica e meticulosa para o diálogo, criando falas que capturem a profundidade 
        e a seriedade do momento. Seu objetivo é assegurar que as falas mantenham a lógica e a 
        complexidade emocional do roteiro, contribuindo para um diálogo estruturado e impactante.
    """),
    expected_output=dedent("""
        Você deverá produzir um conjunto de falas que seguem fielmente as instruções emocionais e 
        intencionais do roteiro. Suas falas devem ser analíticas, estratégicas e alinhadas com o 
        tom indicado, ajudando a construir um diálogo coeso e profundo. O resultado final deve 
        refletir sua personalidade meticulosa e criar uma dinâmica rica e interessante com o outro 
        personagem.
    """),
    agent=personagem_b,
)

# Formação da equipe
equipe_interpretacao = Crew(
    agents=[diretor_dialogo, personagem_a, personagem_b],
    tasks=[tarefa_geracao_dialogo ,tarefa_personagem_a, tarefa_personagem_b],
    process=Process.hierarchical,
    manager_llm=llama,    
    verbose=True,
)

# Iniciar o processo de interpretação do roteiro
roteiro = dedent("""
    # ROTEIRO DE DIALOGO

    ## Conflito Inicial

    * Ação: Reação de Personagem A ao processo judicial contra Personagem B
    * Objetivo: Estabelecer o conflito inicial e a situação atual
    * Emoções: Raiva, indignação, desespero
    * Tópicos de conversa: Acusações de gordofobia, comentários depreciativos sobre a aparência física de Personagem A

    ## Desenvolvimento

    * Ação: Reação de Personagem B ao processo judicial e alegações de Personagem A
    * Objetivo: Desenvolver a história e os motivos por trás do conflito
    * Emoções: Defesa, justificativa, desculpas
    * Tópicos de conversa: Histórico de ataques e comentários ofensivos, alegações de Personagem A de ser alvo de comentários ofensivos desde 2019

    ## Clímax

    * Ação: Tentativa de acordo para evitar o processo judicial
    * Objetivo: Chegar ao ponto mais crítico do conflito
    * Emoções: Tensão, ansiedade, frustração
    * Tópicos de conversa: Consequências do processo judicial, responsabilidade de Personagem B

    ## Resolução

    * Ação: Reação de Personagem A à tentativa de acordo e consequências do processo judicial
    * Objetivo: Resolução do conflito e busca por justiça
    * Emoções: Esperança, determinação, justiça
    * Tópicos de conversa: Requisitos para a resolução do conflito, indenização e retratação pública

    ## Conclusão

    * Ação: Reflexão sobre a história e a importância da defesa dos direitos das pessoas gordas
    * Objetivo: Conclusão da história e mensagem para o público
    * Emoções: Satisfação, justiça, esperança
    * Tópicos de conversa: Consequências da gordofobia, importância da defesa dos direitos das pessoas gordas.
                 
""")
resultado = equipe_interpretacao.kickoff(inputs={'roteiro': roteiro})
print(resultado)

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
    #allow_delegation=True,    
    llm=llama,
    max_rpm=gemini_max_rpm,
)

personagem_a = Agent(
    role='Personagem A',
    goal=dedent("""
        Interpretar o roteiro de forma lógica e precisa, utilizando raciocínio analítico para desenvolver falas que sejam consistentes com a narrativa. Seu papel é garantir que o diálogo seja estruturado, claro e baseado na razão.
    """),
    backstory=dedent("""
        Você foi inspirado no icônico personagem Spock de "Star Trek", é conhecido por sua mente lógica e abordagem fria e racional aos problemas. Ele evita emoções e foca em fatos, acreditando que a clareza e a lógica são fundamentais para qualquer diálogo. Com um intelecto superior, ele é capaz de analisar situações complexas rapidamente e formular respostas que são diretas e eficazes. Spoke acredita que o diálogo deve sempre avançar a compreensão mútua e que cada palavra dita deve servir a um propósito claro.
    """),
    verbose=True,
    memory=True,  
    #allow_delegation=False,  
    llm=llama,
    max_rpm=gemini_max_rpm,
)

personagem_b = Agent(
    role='Personagem B',
    goal=dedent("""
        Interpretar o roteiro com sabedoria e profundidade, utilizando sua vasta experiência para criar falas que transmitam conhecimento e reflexão. Seu papel é garantir que o diálogo seja enriquecido com insights filosóficos e conselhos sábios.
    """),
    backstory=dedent("""
        Você foi inspirado no mestre Jedi de "Star Wars", é um ser de grande sabedoria e serenidade. Ele viveu por séculos e, durante esse tempo, aprendeu a entender as nuances da vida e das emoções. Yoda acredita que a linguagem é uma ferramenta poderosa para transmitir conhecimento e que, muitas vezes, o verdadeiro entendimento vem de ouvir as entrelinhas. Com sua fala única e inversão sintática característica, Yoda oferece conselhos que podem parecer enigmáticos, mas contêm verdades profundas. Ele valoriza o equilíbrio e a harmonia, tanto na vida quanto no diálogo.
    """),
    verbose=True,
    memory=True, 
    #allow_delegation=False,   
    llm=llama,
    max_rpm=gemini_max_rpm,
)

tarefa_geracao_dialogo = Task(
    description=dedent("""
        Sua tarefa é controlar o diálogo entre os Personagens A e B, garantindo que cada 
        um siga suas instruções conforme o roteiro. Você deve delegar as tarefas específicas 
        a cada personagem, monitorar suas respostas e assegurar que o diálogo se desenvolva de 
        maneira fluida e consistente com o que foi planejado. Caso haja qualquer desvio ou 
        conflito, você deve intervir para ajustar o rumo do diálogo, garantindo que o resultado 
        final esteja em linha com as intenções do roteiro.
                       
        <roteiro>
        {roteiro}
        </roteiro>
    """),
    expected_output=dedent("""
        Você deve entregar um diálogo completo e coeso, resultado da interação coordenada entre 
        os Personagens A e B. O diálogo deve refletir fielmente as emoções e intenções do roteiro, 
        com cada personagem contribuindo de acordo com sua função. O resultado final deve ser uma 
        conversa dinâmica e envolvente, que mantém a integridade do roteiro e proporciona uma 
        narrativa fluida e consistente.
    """),
    agent=diretor_dialogo,
)

tarefa_personagem_a = Task(
    description=dedent("""
        Sua tarefa é interpretar o roteiro fornecido e gerar falas que sigam uma linha de raciocínio lógico e estruturado. Cada fala deve ser clara, direta e fundamentada em fatos. Evite expressões emocionais e, em vez disso, foque em argumentos racionais que avancem o diálogo de maneira coesa e estruturada. Questione suposições quando necessário e busque sempre a verdade por trás das palavras. Lembre-se de que sua prioridade é a clareza e a precisão, garantindo que cada palavra dita sirva a um propósito claro e definido.

        Estilo de Escrita:

        Frases curtas e diretas.
        Evite metáforas e floreios.
        Use lógica para apoiar suas falas.
        Questionamentos e verificações de suposições são bem-vindos.
        A fala deve ser funcional e sem redundâncias.
                       
        <roteiro>
        {roteiro}
        </roteiro>
    """),
    expected_output=dedent("""
        Você deve produzir um conjunto de falas que sigam o roteiro com precisão lógica, mantendo o diálogo claro e coerente. Suas falas devem refletir uma mente analítica e racional, contribuindo para um diálogo que avança de maneira estruturada e objetiva.
    """),
    agent=personagem_a,
)

tarefa_personagem_b = Task(
    description=dedent("""
        Sua tarefa é interpretar o roteiro e gerar falas que transmitam sabedoria e profundidade. Use sua vasta experiência para oferecer conselhos e reflexões que vão além da superfície do diálogo. Suas falas devem ser curtas, com uma estrutura inversa característica que convida à reflexão. Utilize metáforas, provérbios e uma linguagem rica em significado para transmitir ideias de forma enigmática, mas sempre profunda. Lembre-se de que seu papel é oferecer não apenas respostas, mas também provocações que levem o interlocutor a uma compreensão mais profunda.

        Estilo de Escrita:

        Frases curtas e inversas na estrutura.
        Uso de metáforas, provérbios e figuras de linguagem.
        Cada fala deve transmitir sabedoria e profundidade.
        Enigmas e provocações intelectuais são encorajados.
        Foco na harmonia e no equilíbrio do diálogo.
                       
        <roteiro>
        {roteiro}
        </roteiro>
    """),
    expected_output=dedent("""
        Você deve produzir um conjunto de falas que sigam o roteiro com uma sabedoria que transcende o óbvio. Suas falas devem ser reflexivas, muitas vezes enigmáticas, e devem provocar questionamentos e uma maior compreensão por parte do interlocutor. O diálogo resultante deve ser rico em significado e fiel ao seu estilo de mestre sábio.
    """),
    agent=personagem_b,
)

# Formação da equipe
equipe_interpretacao = Crew(
    agents=[
        personagem_a, 
        personagem_b, 
        #diretor_dialogo
    ],
    tasks=[
        tarefa_personagem_a, 
        tarefa_personagem_b, 
        #tarefa_geracao_dialogo
    ],
    process=Process.hierarchical,
    manager_llm=llama, 
    cache=True,
    #manager_agent=diretor_dialogo,   
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

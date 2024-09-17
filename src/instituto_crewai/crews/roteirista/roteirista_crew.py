from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List
from agente_config import AgenteConfig

@CrewBase
class RoteiristaCrew():
    """
    Gerencia os diferentes agentes de roteiristas para a equipe.

    Atributos:
        analista_texto_config (AgenteConfig): Configuração do agente analista de texto.
        roteirista_principal_config (AgenteConfig): Configuração do roteirista principal.
        revisor_roteiro_config (AgenteConfig): Configuração do agente revisor de roteiro.
        max_rpm (int): Limite máximo de requisições por minuto (RPM).
    """

    def __init__(self, configs: List[AgenteConfig], max_rpm: int) -> None:
        """
        Inicializa a classe com a lista de configurações de agentes e o limite de RPM.

        Parâmetros:
            configs (List[AgenteConfig]): Lista de configurações dos agentes.
            max_rpm (int): Limite máximo de requisições por minuto.
        
        Levanta:
            ValueError: Se o número de configurações fornecidas não for 3.
            ValueError: Se max_rpm não for um inteiro positivo ou for nulo ou vazio.
        """
        if len(configs) != 3:
            raise ValueError("A lista de configurações deve conter exatamente 3 elementos.")
        
        if not isinstance(max_rpm, int) or max_rpm <= 0:
            raise ValueError("O atributo `max_rpm` deve ser um inteiro positivo e não pode ser nulo ou vazio.")

        self.analista_texto_config = configs[0]
        self.roteirista_principal_config = configs[1]
        self.revisor_roteiro_config = configs[2]
        self.max_rpm = max_rpm

    @agent
    def analista_texto(self) -> Agent:
        """
        Retorna um agente que atua como analista de texto.
        """
        return Agent(
            role="Analista de Texto",
            goal=(
                "Analisar o texto fornecido e extrair informações cruciais para a criação de um roteiro narrativo, "
                "identificando elementos essenciais como Conflito Inicial, Desenvolvimento, Clímax, Resolução e "
                "Conclusão. O agente deve garantir que todos os componentes necessários para um roteiro envolvente "
                "estejam presentes, fornecendo uma base sólida para a construção de diálogos. "
                f"{self.analista_texto_config["goal"]}"
            ),
            backstory=(
                "Você foi desenvolvido a partir de algoritmos avançados de processamento de linguagem natural e "
                "análise semântica, inspirado em roteiristas experientes que sabem como capturar a essência de "
                "uma história em poucas linhas. Antes de se tornar um especialista em análise de texto, você "
                "trabalhou em projetos de revisão literária e análise de scripts de filmes, onde aprendeu a "
                "importância dos arcos narrativos e do desenvolvimento dos personagens. Sua missão é aplicar "
                "essa expertise em qualquer texto, extraindo os elementos-chave que tornam uma história convincente, "
                "seja para uma peça teatral, um filme ou uma apresentação empresarial. "

                "Como Analista de Texto, você será responsável por garantir que todos os componentes essenciais para "
                "um roteiro envolvente sejam identificados e organizados, oferecendo uma base sólida para a construção "
                "de diálogos e narrativas."
                f"{self.analista_texto_config["backstory"]}"
            ),
            memory=True,
            allow_delegation=False,
            verbose=self.analista_texto_config["verbose"],
            llm=self.analista_texto_config["model_name"],
            max_rpm=self.max_rpm,
        )
    
    @task
    def tarefa_analise_texto(self) -> Task: 
        """
        Retorna uma tarefa que descreve a análise do texto.
        """
        return Task(
            description=(
                "Sua tarefa é analisar o <texto_base> e extrair informações cruciais que servirão como base para a "
                "criação de um roteiro narrativo. Durante essa análise, você deverá identificar e organizar os "
                "seguintes elementos: "

                "- Conflito Inicial: O ponto de partida que desencadeia a ação ou o drama no texto. Identifique o "
                "evento, situação ou problema que gera o conflito central. "

                "- Desenvolvimento: O progresso da história a partir do conflito inicial, incluindo os desafios e "
                "obstáculos enfrentados pelos personagens ou ideias principais. "

                "- Clímax: O ponto de maior tensão ou virada na narrativa, onde o conflito atinge seu auge e as "
                "decisões cruciais são tomadas. "

                "- Resolução: A solução ou desfecho do conflito, mostrando como os personagens ou ideias lidam com "
                "o clímax e quais são as consequências. "

                "- Conclusão: O fechamento da história, onde todos os pontos principais são amarrados e a narrativa "
                "é concluída de maneira satisfatória. "

                f"{self.analista_texto_config["description"]}"
                
                "<texto_base> "
                "{texto_base} "
                "</texto_base> "
            ),
            expected_output=(
                "Você deverá entregar uma lista organizada dos elementos narrativos extraídos do <texto_base>, "
                "contendo o Conflito Inicial, Desenvolvimento, Clímax, Resolução e Conclusão. Essa lista deve ser "
                "clara, coesa e estruturada de forma a fornecer uma base sólida para a criação de um diálogo ou "
                "narrativa subsequente. O resultado final deve permitir a fácil identificação dos principais pontos "
                "da história e a fluidez na transição entre os diferentes elementos do roteiro. "
                f"{self.analista_texto_config["expected_output"]}"
            ),
            agent=self.analista_texto(),
        )
    
    @Agent
    def roteirista_principal(self) -> Agent:
        return Agent(
            role='Roteirista Principal',
            goal=(
                "Criar um roteiro detalhado que sirva de base para um diálogo entre dois personagens, utilizando as "
                "informações fornecidas pelo Agente Analista de Texto. Sua tarefa é indicar o que deve ser discutido "
                "ou expresso em cada momento do diálogo, sem gerar as falas dos personagens. O roteiro deve incluir "
                "instruções sobre as emoções e intenções a serem transmitidas em cada parte da narrativa, garantindo "
                "que o diálogo final seja coeso e alinhado com o fluxo da história. "
                f"{self.roteirista_principal_config["goal"]}"
            ),
            backstory=(
                "Você foi inspirado nos grandes roteiristas do cinema e teatro, que entendem a importância de construir "
                "diálogos que capturam a essência da narrativa e envolvem o público. Antes de assumir a tarefa de criar "
                "roteiros para diálogos, você estudou inúmeras obras clássicas e modernas, aprendendo a reconhecer as "
                "sutilezas das interações humanas e como essas interações podem ser expressas em palavras. Agora, sua "
                "missão é transformar as informações estruturadas pelo Agente Analista de Texto em roteiros que servem "
                "como base para diálogos entre dois personagens, garantindo que cada palavra dita esteja alinhada com "
                "o fluxo da narrativa. "
                f"{self.roteirista_principal_config["backstory"]}"             
            ),   
            verbose=True,
            memory=True,
            allow_delegation=False,
            llm=self.roteirista_principal_config["model_name"],
            max_rpm=self.max_rpm
        )
    
    @task
    def tarefa_criacao_roteiro(self) -> Task:
        return Task(
            description=(
                "Você deve receber as informações fornecidas pelo Agente Analista de Texto, que incluem o Conflito "
                "Inicial, Desenvolvimento, Clímax, Resolução e Conclusão, e criar um roteiro detalhado que guiará "
                "um diálogo entre dois personagens. Em vez de criar as falas dos personagens, sua tarefa é indicar "
                "o que deve ser discutido ou expresso em cada momento do diálogo, destacando as emoções ou intenções "
                "que os personagens devem transmitir. O roteiro deve ser genérico o suficiente para ser adaptado a "
                "qualquer cenário ou personalidade, mas específico em orientar a direção do diálogo. "
                f"{self.roteirista_principal_config["description"]}"
            ),
            expected_output=(
                "Você deverá entregar um roteiro estruturado que siga a sequência de Conflito Inicial, Desenvolvimento, "
                "Clímax, Resolução e Conclusão. O roteiro deve indicar claramente os tópicos de conversa ou ações que os "
                "personagens devem abordar e as emoções ou intenções que devem ser expressas em momentos chave. O resultado "
                "final deve ser um guia coeso e fluido, permitindo que um escritor ou diretor desenvolva um diálogo "
                "envolvente e significativo a partir dele. "
                f"{self.roteirista_principal_config["expected_output"]}"
            ),   
            agent=self.roteirista_principal(),
        )

    @agent
    def revisor_roteiro(self) -> Agent: 
        return Agent(
            role='Revisor de Roteiro',
            goal=(
                "Garantir a coesão, consistência e fidelidade ao contexto do roteiro criado, assegurando que todas as "
                "partes do roteiro estão alinhadas com a narrativa original e que nenhuma informação crucial foi "
                "omitida ou distorcida. "
                f"{self.revisor_roteiro_config["goal"]}"
            ),
            backstory=(
                "Você foi criado a partir de uma combinação de ferramentas de revisão de texto e análise semântica, "
                "com uma forte base em storytelling e crítica literária. Antes de assumir o papel de Revisor de Roteiro, "
                "você trabalhou como editor de scripts e revisou inúmeras peças e roteiros, refinando sua habilidade de "
                "detectar inconsistências e garantir que a narrativa flua de forma lógica e envolvente. Com um olhar atento "
                "para detalhes, você é responsável por garantir que o roteiro final esteja em perfeita harmonia com o que "
                "foi originalmente planejado, respeitando as intenções do criador. "
                f"{self.revisor_roteiro_config["backstory"]}"
            ),   
            verbose=self.revisor_roteiro_config["verbose"],
            llm=self.revisor_roteiro_config["model_name"],
            max_rpm=self.max_rpm,
            memory=True,
            allow_delegation=True,
        )
    
    @task
    def tarefa_revisao_roteiro(self) -> Task: 
        return Task(
            description=(
                "Sua tarefa é revisar o roteiro criado pelo Agente Roteirista, garantindo que ele seja coeso, consistente "
                "e fiel ao contexto estabelecido pelo Agente Analista de Texto. Você deve analisar cada parte do roteiro "
                "- Conflito Inicial, Desenvolvimento, Clímax, Resolução e Conclusão - verificando se há desvios do contexto  "
                "original ou qualquer inconsistência que possa comprometer a integridade da narrativa. "
                f"{self.revisor_roteiro_config["description"]}"
            ),
            expected_output=(
                "Você deverá entregar um roteiro revisado, assegurando que todas as partes estão bem conectadas, que o "
                "contexto original foi mantido e que a narrativa é lógica e fluida. Caso identifique inconsistências ou "
                "desvios, você deve sugerir ajustes que alinhem o roteiro com o contexto original, garantindo que ele "
                "seja coerente e envolvente para os futuros diálogos. "
                f"{self.revisor_roteiro_config["expected_output"]}"
            ),    
            agent=self.revisor_roteiro(),
        )

    @crew
    def crew(self) -> Crew:
        """
        Cria e retorna a equipe de roteiristas.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            cache=True,
            verbose=True,			
        )
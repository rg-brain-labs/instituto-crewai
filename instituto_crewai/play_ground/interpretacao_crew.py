from crewai import Agent, Task, Crew, Process
from textwrap3 import dedent

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
)

tarefa_geracao_dialogo = Task(
    description=dedent("""
        Vocês devem trabalhar juntos para seguir o <roteiro> fornecido e gerar as falas que 
        compõem o diálogo. Cada um de vocês deve interpretar as emoções e intenções 
        indicadas no roteiro, adaptando-as à sua própria perspectiva e estilo. Enquanto o 
        Personagem A traz uma abordagem mais leve e espontânea ao diálogo, o Personagem B 
        deve manter uma postura mais séria e estratégica. A interação entre vocês deve 
        refletir a dinâmica indicada no roteiro, criando um diálogo coeso e envolvente que 
        respeita as emoções e intenções estabelecidas.
                       
        <roteiro>
        {roteiro}
        </roteiro>
    """),
    expected_output=dedent("""
        Vocês devem produzir um diálogo completo, em que cada fala reflita fielmente as 
        instruções emocionais e intencionais do roteiro. O diálogo final deve capturar a 
        dinâmica entre os dois personagens, com o Personagem A contribuindo com falas 
        criativas e leves, e o Personagem B trazendo profundidade e estrutura ao diálogo. 
        O resultado final deve ser um diálogo fluido, coeso e alinhado com o roteiro, que 
        combina as forças e características únicas de ambos os personagens.
    """),
    agent=[personagem_a, personagem_b],
)

# Formação da equipe
equipe_interpretacao = Crew(
    agents=[personagem_a, personagem_b],
    tasks=[tarefa_geracao_dialogo],
    process=Process.sequential
)

# Iniciar o processo de interpretação do roteiro
roteiro = dedent("""""")
resultado = equipe_interpretacao.kickoff(inputs={'roteiro': roteiro})
print(resultado)

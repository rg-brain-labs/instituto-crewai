from .roteirista_crew import RoteiristaCrew
from .roteirista_config import default_config
from typing import Any

def criar_e_executar_crew(texto_base: str) -> Any:
    # Obtém a configuração padrão
    roteirista_config = default_config()

    # Extrai os valores necessários do dicionário de configuração
    max_rpm = roteirista_config['max_rpm']
    agentes_config = roteirista_config['agente_config']

    # Cria a instância de RoteiristaCrew
    crew = RoteiristaCrew(agentes_config, max_rpm).crew()

    # Executa a crew com o texto base
    resultado = crew.kickoff(inputs={'texto_base': texto_base})

    return resultado

def main():
    texto_base =(
        "Thaís Carla processa Danilo Gentili por gordofobia. "

        "A dançarina e influenciadora digital Thaís Carla entrou com um processo judicial contra o "
        "apresentador Danilo Gentili no Tribunal de Justiça da Bahia (TJ-BA), acusando-o de praticar " 
        "gordofobia. O apresentador do programa The Noite, do SBT, já havia sido processado por Thaís "
        "anteriormente pelo mesmo motivo. "

        "Desta vez, a influenciadora está solicitando uma retratação pública nas redes sociais de "
        "Gentili, além de uma indenização no valor de R$ 15 mil. Segundo informações dos portais F5, "
        "da Folha de S.Paulo, e Metrópoles, Thaís acusa o apresentador de fazer comentários depreciativos "
        "sobre sua aparência física, o que, segundo ela, fomenta ataques contra sua pessoa. "

        "Desde 2019, Thaís Carla alega ser alvo de comentários ofensivos de Gentili, que foi obrigado, "
        "há dois anos, a apagar imagens dela após uma decisão judicial. No último dia 27, foi feita uma "
        "tentativa de acordo para evitar o processo judicial, mas sem sucesso. Ainda não há previsão "
        "para o julgamento, mas a influenciadora espera que a situação seja resolvida rapidamente. "

        "Thaís Carla é uma figura conhecida na mídia por defender os direitos das pessoas gordas e "
        "ganhou destaque ao aparecer no programa Domingão do Faustão, da TV Globo, no final dos anos "
        "2010. Ela também integrou o balé da cantora Anitta entre 2017 e 2019, além de participar de "
        "diversos outros programas de televisão. "
    )
    
    
    resultado = criar_e_executar_crew(texto_base)

    print(resultado)

if __name__ == '__main__':
    main()
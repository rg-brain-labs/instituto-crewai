from instituto_crewai.equipes import RoteiristaController
import json

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


crew = RoteiristaController()
#crew.train(3, "teste_train", {'texto_base': texto_base})
crew_result = crew.run({'texto_base': texto_base})

# Accessing the crew output
#print(f"Raw Output: {crew_result.raw}")
# if crew_result.json_dict:
#     print(f"JSON Output: {json.dumps(crew_result.json_dict, indent=2)}")
# if crew_result.pydantic:
#     print(f"Pydantic Output: {crew_result.pydantic}")
print(f"Tasks Output: {crew_result.tasks_output}")
#print(f"Token Usage: {crew_result.token_usage}")

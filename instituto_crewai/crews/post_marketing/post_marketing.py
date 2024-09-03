from crew import PostMarketigCrew

def run():    
    inputs = {
        'dominio_cliente': 'consorciouniao.com.br',
        'descricao_projeto': """
Consórcio União, é uma empresa de consórcio que está a 45 anos no mercado. Sempre lançando produtos inovadores 

Domínio do Cliente: Venda de Consórcios
Visão Geral do Projeto: Criar uma campanha de marketing para educar financeiramente as pessoas e falar como o consórcio pode ajudar.
"""
    }
    PostMarketigCrew().crew().kickoff(inputs=inputs)

    
run()
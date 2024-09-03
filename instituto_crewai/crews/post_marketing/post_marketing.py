import sys
from crew import PostMarketigCrew
# from dotenv import load_dotenv
# from pathlib import Path

# # Carrega variáveis de ambiente
# dotenv_path = Path(__file__).parent.parent.parent / 'config' / '.env'
# load_dotenv(dotenv_path)

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


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         'customer_domain': 'crewai.com',
#         'descricao_projeto': """
# CrewAI, a leading provider of multi-agent systems, aims to revolutionize marketing automation for its enterprise clients. This project involves developing an innovative marketing strategy to showcase CrewAI's advanced AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities. The campaign will target tech-savvy decision-makers in medium to large enterprises, highlighting success stories and the transformative potential of CrewAI's platform.

# Customer Domain: AI and Automation Solutions
# Project Overview: Creating a comprehensive marketing campaign to boost awareness and adoption of CrewAI's services among enterprise clients.
# """
#     }
#     try:
#         PostMarketigCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")
    
run()

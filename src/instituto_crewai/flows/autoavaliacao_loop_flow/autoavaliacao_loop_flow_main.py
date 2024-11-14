from typing import Optional

from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

from .equipes.shakespeare_crew.shakespeare_crew import ShakespeareCrew

class EstatoFlowPostagemShakespeareX(BaseModel):
    postagem_x: str = ""
    feedback: Optional[str] = None
    validade: bool = False
    contagem_tentativas: int = 0

class AutoAvaliacaoLoopFlow(Flow[EstatoFlowPostagemShakespeareX ]):

    @start("tentar_novamente")
    def criar_post_x_shakespeare(self):
        ShakespeareCrew().crew().kickoff(inputs={"topico": "Dinossáuros na Terra Média", "feedback": self.state.feedback})

    @router(criar_post_x_shakespeare)
    def avaliar_x_post(self):
        #TODO IMPLEMENTAR
        pass

    @listen("completado")
    def salvar_resulado(self):
        # TODO IMPLEMENTAR
        pass
    
    @listen("maximo_tentativas_excedido")
    def saida_maximo_tentativas_excedido(self):
        # TODO IMPLEMENTAR
        pass

from typing import Optional

from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

from instituto_crewai.flows.autoavaliacao_loop_flow.equipes.shakespeare_crew.shakespeare_crew import ShakespeareCrew
from instituto_crewai.flows.autoavaliacao_loop_flow.equipes.revisao_post_x_crew.revisao_post_x_crew import RevisaoPostXCrew

class EstatoFlowPostagemShakespeareX(BaseModel):
    postagem_x: str = ""
    feedback: Optional[str] = None
    validade: bool = False
    contagem_tentativas: int = 0

class AutoAvaliacaoLoopFlow(Flow[EstatoFlowPostagemShakespeareX ]):

    @start("tentar_novamente")
    def criar_post_x_shakespeare(self):
        postagem_x = (
            ShakespeareCrew()
            .crew()
            .kickoff(inputs={"tópico": "Dinossáuros na Terra Média", "feedback": self.state.feedback})
        )
        
        print(f"Postagem {postagem_x}")
        
        self.state.postagem_x = postagem_x.raw

    @router(criar_post_x_shakespeare)
    def avaliar_x_post(self):
        if self.state.contagem_tentativas > 3:
            return "maximo_tentativas_excedido"
        
        avaliacao = RevisaoPostXCrew().crew().kickoff(inputs={"postagem_x": self.state.postagem_x})
        
        self.state.validade = avaliacao["validade"]
        self.state.feedback = avaliacao["feedback"]
        
        print(f"Validade {self.state.validade}")
        print(f"feedback {self.state.feedback}")
        
        if self.state.validade:
            return "completado"
        
        self.state.contagem_tentativas += 1
        print("tentar_novamente")
        
        return "tentar_novamente"

    @listen("completado")
    def salvar_resulado(self):
        print("Postagem X é valida")
        print(f"Postagem X {self.state.postagem_x}")
        
        with open("postagem_x.md", "w") as postagem:
            postagem.write(self.state.postagem_x)
    
    @listen("maximo_tentativas_excedido")
    def saida_maximo_tentativas_excedido(self):
        print("Número máximo de tentativas excedido")
        print(f"Postagem X {self.state.postagem_x}")
        print(f"Feedback {self.state.feedback}")
        
def kickoff():
    auto_avaliacao_flow = AutoAvaliacaoLoopFlow()
    auto_avaliacao_flow.kickoff()


def plot():
    auto_avaliacao_flow = AutoAvaliacaoLoopFlow()
    auto_avaliacao_flow.plot()


if __name__ == "__main__":
    kickoff()
        

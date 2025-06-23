from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

from ..equipes.equipe_classificadora.equipe_classificadora import EquipeClassificadora
from ..equipes.equipe_ajuda.equipe_ajuda import EquipeAjuda

class Classificacao(BaseModel):
    classificacao: str = ""

class ConsultorConsorcioFlow(Flow[Classificacao]):
    
    @start()
    def classificar_solicitacao(self):       
        equipe_classificadora = EquipeClassificadora()
        classificacao_equipe = equipe_classificadora.crew().kickoff(inputs={"solicitacao": "Boa tarde, gostaria de saber sobre como funciona a VSS Poseidon"})
        classificacao = classificacao_equipe.raw       
        self.state.classificacao = classificacao

    @router(classificar_solicitacao)
    def roteador(self):       
        if self.state.classificacao == "DUVIDA_CONSORCIO":
            return "DUVIDA_CONSORCIO"
        else:
            return "DUVIDA_OUTRA_COISA"
    
    @listen("DUVIDA_CONSORCIO")
    def duvida_consorcio(self):        
        return f"O Cliente quer falar sobre Consórcio"
    
    @listen("DUVIDA_OUTRA_COISA")
    def nao_classificado(self):  
        equipe_ajuda = EquipeAjuda(self.state.classificacao)
        mensagem_ajuda = equipe_ajuda.crew().kickoff()     
        return mensagem_ajuda.raw
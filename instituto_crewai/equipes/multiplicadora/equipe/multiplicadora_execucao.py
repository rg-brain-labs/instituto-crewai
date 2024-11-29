from .multiplicadora_equipe import EquipeMultiplicadora

class ExecucaoMultiplicadora:
    def __init__(self):
        self.equipe = EquipeMultiplicadora().equipe()

    def executar(self):        
        return self.equipe.kickoff()
from .brian_consultor_flows import ConsultorConsorcioFlow

class BrianConsultorExecucao:
    def __init__(self, solicitacao):
        self.solicitacao = solicitacao
        self.consultor_consorcio_flow = ConsultorConsorcioFlow()

    def executar_consultor_consorcio_flow(self):        
        return self.consultor_consorcio_flow.kickoff()
from crewai.flow.flow import Flow, listen, router, start
from litellm import completion
from pydantic import BaseModel

class Classificacao(BaseModel):
    classificacao: str = ""

class ConsultorConsorcioFlow(Flow[Classificacao]):

    model = "gemini/gemini-1.5-flash"
    
    @start()
    def classificar_solicitacao(self):

        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": """
                    Voce recebeu uma solicitação de um cliente e precisa classificar a solicitação, 
                    identifique se o cliente solicitou algo sobre Consórcio ou alguma outra coisa.

                    Retorne somente uma das seguintes opções: 
                        - DUVIDA_CONSORCIO
                        - DUVIDA_OUTRA_COISA

                    Você so precisa classeficar e retornar uma da opções acima.

                    ## Solicitação ##
                    Gostaria de saber como funciona o Consórcio da empresa XYZ.
                    """,
                },
            ],
        )

        classificacao = response["choices"][0]["message"]["content"]
        print(f"A classificação foi: {classificacao}")
        self.state.classificacao = classificacao

    @router(classificar_solicitacao)
    def roteador(self):
        print(f"roteador deve retornar {self.state.classificacao}")
        if self.state.classificacao == "DUVIDA_CONSORCIO":
            return "DUVIDA_CONSORCIO"
        else:
            return "DUVIDA_OUTRA_COISA"
    
    @listen("DUVIDA_CONSORCIO")
    def duvida_consorcio(self):        
        return f"O Cliente quer falar sobre Consórcio"
    
    @listen("DUVIDA_OUTRA_COISA")
    def nao_classificado(self):       
        return f"O cliente não quer falar sobre consorcio"
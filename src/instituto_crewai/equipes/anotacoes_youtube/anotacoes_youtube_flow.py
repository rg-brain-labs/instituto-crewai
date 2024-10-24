from crewai.flow.flow import Flow, listen, start
from litellm import completion
import asyncio
from youtube_transcript_api import YouTubeTranscriptApi

class ExampleFlow(Flow):
    model = "gemini/gemini-1.5-pro"  
    
    def __init__(self, id_video, fonte_transcricao, idioma):
        super().__init__()
        self.id_video = id_video
        self.fonte_transcricao = fonte_transcricao
        self.idioma = idioma

    @start()
    def obter_transcricao_video(self):         
        transcricao = YouTubeTranscriptApi.get_transcript(self.id_video, languages=['pt'])
             

        return ' '.join(item['text'] for item in transcricao)
    
    @listen(obter_transcricao_video)
    def equipe_corretora(self, transcricao):
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": 
                        f"<transcricao>{transcricao}</transcricao> " +
                        f"<fonte_transcricao>{self.fonte_transcricao}</fonte_transcricao> " +   
                        f"<idioma>{self.idioma}</idioma> "                     
                        "Você é um corretor ortográfico e gramatical especializado em revisar textos de <fonte_transcricao>. " + 
                        "Sua tarefa é revisar a <transcricao> que está em <idioma>, corrigindo erros ortográficos, gramaticais " + 
                        "e de pontuação, mantendo o estilo e a fluidez do autor. " +
                        "Se houver inconsistências no estilo (ex: uso de diferentes formas verbais ou tons), ajuste para garantir " + 
                        "uniformidade. Caso encontre frases ambíguas ou confusas, reescreva-as de forma clara e coesa. " +
                        "Além das correções ortográficas, sugira melhorias no texto para aprimorar sua clareza e fluidez, sempre " + 
                        "mantendo o tom original (formal/informal). " #Um exemplo de como a correção deve ser feita é [incluir exemplo].
                        "Lembre-se de priorizar clareza, uniformidade e fluidez durante a correção, sem modificar o conteúdo original do autor.",
                },
            ],
        )

        return response["choices"][0]["message"]["content"]  
    
    @listen(equipe_corretora)
    def equipe_analista_texto(self, transcricao_corrigida):
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content":
                        f"<transcricao_corrigida>{transcricao_corrigida}</transcricao_corrigida> " +
                        f"<idioma>{self.idioma}</idioma> "   
                        "Você é um especialista em análise de texto e sua tarefa é extrair os pontos principais do seguinte texto " +
                        "em <idioma>. Analise o texto e identifique os elementos-chave, como temas centrais, argumentos importantes, " + 
                        "e informações relevantes. Com base nesses pontos, faça um resumo conciso que capture a essência do conteúdo " +
                        "original, mantendo a clareza e coerência. " +
                        "Em seguida, retorne o resumo formatado em Markdown. Estruture o texto em seções claras, utilizando cabeçalhos " +
                        "apropriados, listas e negrito quando necessário. O resumo deve ser fácil de ler e entender, mesmo sem o texto original. " +
                        " Lembre-se de seguir esta estrutura para o retorno: " +
                        "Pontos Principais: Liste os principais pontos do texto. " +
                        "Resumo: Um resumo coeso e conciso com as informações principais. " +
                        "Formato Markdown: Utilize cabeçalhos, listas e negrito para organizar o resumo. " +
                        "Exemplo de formatação esperada: " +                        
                        "## Pontos Principais " +
                        "- [Ponto principal 1] " +
                        "- [Ponto principal 2] " +
                        "- [Ponto principal 3] " +
                        "## Resumo " +
                        "[Resumo conciso baseado nos pontos principais] " +
                        "Certifique-se de manter o texto claro, coeso e organizado"
                }
            ]
        )
        
        return response["choices"][0]["message"]["content"]        

async def main():
    flow = ExampleFlow("n2gHKJwBCP4", "YouTube", "pt-br")
    resultado_flow = await flow.kickoff()
    
    print(resultado_flow)

asyncio.run(main())
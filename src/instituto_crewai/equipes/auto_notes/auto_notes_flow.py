from crewai.flow.flow import Flow, listen, start
from litellm import completion
from youtube_transcript_api import YouTubeTranscriptApi
import os
from datetime import datetime
from pathlib import Path

class AutoNotes(Flow):
    model = "gemini/gemini-1.5-pro"  
    
    def __init__(self, id_video, fonte_transcricao, idioma_origem):
        super().__init__()
        self.id_video = id_video
        self.fonte_transcricao = fonte_transcricao
        self.idioma_origem = idioma_origem
        self.max_tokens = 8000
        
    def salvar_arquivo(self, conteudo, nome_arquivo):
        """
        Salva um arquivo em uma pasta padrão dentro de 'Documents/arquivos_salvos'.
        
        Args:
            conteudo: O conteúdo a ser salvo no arquivo (str ou bytes)
            nome_arquivo: Nome do arquivo com extensão (ex: 'teste.txt')
            
        Returns:
            str: Caminho completo onde o arquivo foi salvo
            
        Raises:
            OSError: Se houver erro ao criar diretório ou salvar arquivo
        """
        # Definir pasta padrão na pasta Documents
        pasta_padrao = os.path.join(str(Path(__file__).parent), "arquivos")
        
        # Criar pasta se não existir
        if not os.path.exists(pasta_padrao):
            os.makedirs(pasta_padrao)
        
        # Adicionar data ao nome do arquivo para evitar sobrescrita
        nome_base, extensao = os.path.splitext(nome_arquivo)
        data_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_final = f"{nome_base}_{data_atual}{extensao}"
        
        # Caminho completo do arquivo
        caminho_completo = os.path.join(pasta_padrao, nome_final)
        
        # Determinar modo de escrita baseado no tipo do conteúdo
        modo = 'wb' if isinstance(conteudo, bytes) else 'w'
        
        # Salvar arquivo
        try:
            with open(caminho_completo, modo) as arquivo:
                arquivo.write(conteudo)
            return caminho_completo
        except Exception as e:
            raise OSError(f"Erro ao salvar arquivo: {str(e)}")

    @start()
    def obter_transcricao_video(self):         
        transcricao = YouTubeTranscriptApi.get_transcript(self.id_video, languages=['en'])        
        texto_transcrito =  ' '.join(item['text'] for item in transcricao)
        
        self.salvar_arquivo(texto_transcrito, "texto_transcrito.txt")
        
        return texto_transcrito
    
    @listen(obter_transcricao_video)
    def equipe_corretora(self, transcricao):
        texto_corrigido_completo = ""
        texto_restante = transcricao
        
        while len(texto_restante) > 0:
            print(texto_restante)
            print("--------------------------\n\n\n")
             # Faz a chamada ao modelo para processar um pedaço do texto.
            response = completion(
                model=self.model,
                max_completion_tokens=self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": 
                            f"<transcricao>{texto_restante[:self.max_tokens]}</transcricao> " +
                            f"<fonte_transcricao>{self.fonte_transcricao}</fonte_transcricao> " +   
                            f"<idioma>{self.idioma_origem}</idioma> "                     
                            "Você é um corretor ortográfico e gramatical especializado em revisar textos de <fonte_transcricao>. " + 
                            "Sua tarefa é revisar a <transcricao> que está em <idioma>, corrigindo erros ortográficos, gramaticais " + 
                            "e de pontuação, mantendo o estilo e a fluidez do autor. " +
                            "Se houver inconsistências no estilo (ex: uso de diferentes formas verbais ou tons), ajuste para garantir " + 
                            "uniformidade. Caso encontre frases ambíguas ou confusas, reescreva-as de forma clara e coesa. " +
                            "Além das correções ortográficas, sugira melhorias no texto para aprimorar sua clareza e fluidez, sempre " + 
                            "mantendo o tom original. " 
                            "Lembre-se de priorizar clareza, uniformidade e fluidez durante a correção, sem modificar o conteúdo original do autor.",
                    },
                ],
            )
            
            # Armazena o pedaço corrigido
            texto_corrigido = response["choices"][0]["message"]["content"]
            texto_corrigido_completo += texto_corrigido
            
            # Atualiza o texto restante removendo a parte já processada
            texto_restante = texto_restante[len(texto_corrigido):]        
       
        
        # Salva o texto completo corrigido
        self.salvar_arquivo(texto_corrigido_completo, "texto_corrigido_completo.txt")

        return texto_corrigido_completo
    
    # @listen(equipe_corretora)
    # def equipe_tradutora(self, transcricao_corrigida):
    #     response = completion(
    #         model=self.model,
    #         max_completion_tokens=32000,
    #         max_tokens=32000,
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content":
    #                     f"<transcricao_corrigida>{transcricao_corrigida}</transcricao_corrigida> " +
    #                     f"<idioma_origem>{self.idioma_origem}</idioma_origem> "  + 
    #                     f"<idioma_destino>pt-br</idioma_destino> " +
    #                     "Você é um tradutor especializado em vídeos do YouTube Sua tarefa é traduzir " +
    #                     "o seguinte <transcricao_corrigida> de <idioma_origem> para <idioma_destino>, " +
    #                     "mantendo a fluidez e o tom apropriado ao contexto do texto. " +
    #                     "Se houver expressões idiomáticas ou frases que não possuem uma tradução literal " + 
    #                     "direta, adapte-as para manter o significado e a naturalidade na língua de destino. " +
    #                     "Além disso, mantenha  o tom como o original, e se necessário, faça breves notas " + 
    #                     "explicativas para destacar nuances culturais ou termos complexos. Um exemplo de " +
    #                     "tradução esperada seria " +
    #                     "Original Hey guys, what's up? Today I'm going to show you how to create a website " + 
    #                     "in just 5 minutes! " +
    #                     "Tradução esperada: Hey pessoal, tudo bem? Hoje eu vou mostrar como criar um site em " +
    #                     "apenas 5 minutos!"
    #             }
    #         ]
    #     )
        
    #     texto_traduzido = response["choices"][0]["message"]["content"]        
    #     self.salvar_arquivo(texto_traduzido, "texto_traduzido.txt")
        
    #     return texto_traduzido
    
    # @listen(equipe_tradutora)
    # def equipe_analista_texto(self, transcricao_corrigida):
    #     response = completion(
    #         model=self.model,
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content":
    #                     f"<transcricao_corrigida>{transcricao_corrigida}</transcricao_corrigida> " +
    #                     f"<idioma>{self.idioma_origem}</idioma> "   
    #                     "Você é um especialista em análise de texto e sua tarefa é extrair os pontos principais do seguinte texto " +
    #                     "em <idioma>. Analise o texto e identifique os elementos-chave, como temas centrais, argumentos importantes, " + 
    #                     "e informações relevantes. Com base nesses pontos, faça um resumo conciso que capture a essência do conteúdo " +
    #                     "original, mantendo a clareza e coerência. " +
    #                     "Em seguida, retorne o resumo formatado em Markdown. Estruture o texto em seções claras, utilizando cabeçalhos " +
    #                     "apropriados, listas e negrito quando necessário. O resumo deve ser fácil de ler e entender, mesmo sem o texto original. " +
    #                     " Lembre-se de seguir esta estrutura para o retorno: " +
    #                     "Pontos Principais: Liste os principais pontos do texto. " +
    #                     "Resumo: Um resumo coeso e conciso com as informações principais. " +
    #                     "Formato Markdown: Utilize cabeçalhos, listas e negrito para organizar o resumo. " +
    #                     "Exemplo de formatação esperada: " +                        
    #                     "## Pontos Principais " +
    #                     "- [Ponto principal 1] " +
    #                     "- [Ponto principal 2] " +
    #                     "- [Ponto principal 3] " +
    #                     "## Resumo " +
    #                     "[Resumo conciso baseado nos pontos principais] " +
    #                     "Certifique-se de manter o texto claro, coeso e organizado"
    #             }
    #         ]
    #     )
        
    #     texto_analisado = response["choices"][0]["message"]["content"]
    #     self.salvar_arquivo(texto_analisado, "texto_analisado.md")
        
    #     return texto_analisado


flow = AutoNotes("n2gHKJwBCP4", "YouTube", "en")
resultado_flow = flow.kickoff()

print(resultado_flow)


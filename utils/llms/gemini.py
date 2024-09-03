from enum import Enum

class GeminiModels(Enum):
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_1_0_PRO = "gemini-1.0-pro"
    
    @property
    def max_rpm(self):
        max_rpm_values = {
            "gemini-1.5-pro": 2,
            "gemini-1.5-flash": 15,
            "gemini-1.0-pro": 15
        }
        return max_rpm_values[self.value]
    
class Gemini():
    def __init__(self, modelo):
        self.modelo = modelo      

    def create_instance(self):
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        return ChatGoogleGenerativeAI(
            model=self.modelo.value,
            verbose=True,
            temperature=0.5,
            # top_p=0.95,
            # top_k=64,
        )
        
#       Top-k:
# O que é: Top-k é uma técnica de amostragem que considera apenas os k tokens mais prováveis ​​do vocabulário para gerar o próximo token.
# Como funciona: O modelo gera uma lista de todas as possíveis palavras que podem vir em seguida, e seleciona as k mais prováveis. A partir desta lista, o modelo escolhe aleatoriamente uma palavra.
# Efeito: Quanto menor o valor de k, menos aleatório e mais previsível o texto gerado será. Um valor alto de k permite mais criatividade e variedade, mas pode resultar em texto menos coerente.  

# Top-p (Nucleus Sampling):
# O que é: Top-p é uma técnica de amostragem que considera todos os tokens cuja probabilidade acumulada é menor que um determinado valor p.
# Como funciona: O modelo calcula a probabilidade de cada palavra, e ordena as palavras em ordem decrescente de probabilidade. Depois, ele calcula a probabilidade acumulada de cada palavra, começando da palavra mais provável. O modelo então considera apenas as palavras cuja probabilidade acumulada seja menor que p.
# Efeito: Top-p é uma abordagem mais suave que top-k, permitindo uma maior variedade de palavras que top-k. Ele permite que o modelo escolha palavras menos prováveis, mas com uma probabilidade acumulada dentro do limite de p.
# Em resumo:
# Top-k é um método mais simples que escolhe entre um conjunto fixo de palavras, resultando em um texto mais previsível.
# Top-p é mais flexível, permitindo a escolha de palavras menos prováveis, mas dentro de um limiar de probabilidade.
# Usando os parâmetros:
# Menor top-k / p: Resulta em um texto mais previsível e menos criativo.
# Maior top-k / p: Resulta em um texto mais criativo e diversificado, mas potencialmente menos coerente.
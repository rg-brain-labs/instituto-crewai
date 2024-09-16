from typing import Any, Dict
from langchain_google_genai import ChatGoogleGenerativeAI

# Definição de constantes para os modelos
GEMINI_1_5_PRO = "gemini-1.5-pro"
GEMINI_1_5_FLASH = "gemini-1.5-flash"
GEMINI_1_0_PRO = "gemini-1.0-pro"

class Gemini:
    """
    Classe para gerenciar e instanciar os modelos Gemini com suas respectivas configurações.

    Atributos:
        temperature (float): Temperatura de geração do modelo.
        models (Dict[str, Dict[str, Any]]): Mapeamento dos modelos Gemini com suas configurações.
        current_model_key (str): Chave atual do modelo selecionado.
    """

    def __init__(self, temperature: float, model_key: str) -> None:
        """
        Inicializa a classe Gemini com a temperatura e o modelo especificado.

        Parâmetros:
            temperature (float): Temperatura de geração para os modelos.
            model_key (str): Chave do modelo a ser instanciado.
        """
        self.temperature = temperature
        self.models: Dict[str, Dict[str, Any]] = {
            GEMINI_1_5_PRO: {
                "model_name": GEMINI_1_5_PRO,
                "rpm": 2,
                "verbose": True,  
            },
            GEMINI_1_5_FLASH: {
                "model_name": GEMINI_1_5_FLASH,
                "rpm": 15,
                "verbose": True,
            },
            GEMINI_1_0_PRO: {
                "model_name": GEMINI_1_0_PRO,
                "rpm": 15,
                "verbose": True,
            },
        }

        self.set_model(model_key)

    def set_model(self, model_key: str) -> None:
        """
        Define o modelo a ser utilizado com base no model_key.

        Parâmetros:
            model_key (str): Chave do modelo a ser utilizado.

        Levanta:
            ValueError: Se o `model_key` não for encontrado nos modelos disponíveis.
        """
        if model_key not in self.models:
            raise ValueError(f"Modelo `{model_key}` não encontrado.")
        
        self.current_model_key = model_key

    def get_instance(self) -> ChatGoogleGenerativeAI:
        """
        Retorna uma instância configurada do modelo atualmente selecionado.

        Retorna:
            ChatGoogleGenerativeAI: Instância configurada do modelo.

        Levanta:
            ValueError: Se nenhum modelo foi definido.
        """
        model_info = self.models[self.current_model_key]
        return ChatGoogleGenerativeAI(
            model=model_info["model_name"],
            temperature=self.temperature,
            verbose=model_info["verbose"],
        )

    def get_model_rpm(self) -> int:
        """
        Retorna o valor de RPM (Requests per Minute) para o modelo atualmente selecionado.

        Retorna:
            int: Valor de RPM do modelo.

        Levanta:
            ValueError: Se nenhum modelo foi definido.
        """
        model_info = self.models[self.current_model_key]
        return model_info["rpm"]
        
# Top-k:
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
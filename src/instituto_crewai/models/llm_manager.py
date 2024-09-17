from typing import Any, Dict


class LLMManager:
    """
    Classe base para gerenciar e instanciar modelos LLM (Large Language Model) com suas respectivas configurações.

    Atributos:
        temperature (float): Temperatura de geração do modelo.
        models (Dict[str, Dict[str, Any]]): Mapeamento dos modelos com suas configurações.
        current_model_key (str): Chave atual do modelo selecionado.
    """

    def __init__(self, temperature: float, model_key: str, models: Dict[str, Dict[str, Any]]) -> None:
        """
        Inicializa a classe LLMManager com a temperatura e os modelos especificados.

        Parâmetros:
            temperature (float): Temperatura de geração para os modelos.
            model_key (str): Chave do modelo a ser instanciado.
            models (Dict[str, Dict[str, Any]]): Configurações de cada modelo.
        """
        self.temperature = temperature
        self.models = models
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

    def get_instance(self, llm_class: Any) -> Any:
        """
        Retorna uma instância configurada do modelo atualmente selecionado.

        Parâmetros:
            llm_class (Any): Classe do LLM a ser instanciada.

        Retorna:
            Any: Instância configurada do modelo LLM.
        """
        model_info = self.models[self.current_model_key]
        return llm_class(
            model=model_info["model_name"],
            temperature=self.temperature,
            verbose=model_info["verbose"],
        )

    def get_model_rpm(self) -> int:
        """
        Retorna o valor de RPM (Requests per Minute) para o modelo atualmente selecionado.

        Retorna:
            int: Valor de RPM do modelo.
        """
        model_info = self.models[self.current_model_key]
        return model_info["rpm"]

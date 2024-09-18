from typing import Dict, Any
from .agente_config import AgenteConfig
from models import GroqManager, LLMA3_8

def default_config() -> Dict[str, Any]:
    """
    Função que retorna a configuração padrão para o roteirista.

    Retorna:
        Dict[str, Any]: Um dicionário contendo 'max_rpm' e a lista 'agente_config'.
    """
    llm_manager = GroqManager(temperature=0.75, model_key=LLMA3_8)
    llm_instance = llm_manager.get_instance()
    
    return {
        'max_rpm': llm_manager.get_model_rpm(),
        'agente_config': [AgenteConfig(llm=llm_instance) for _ in range(3)]
    }

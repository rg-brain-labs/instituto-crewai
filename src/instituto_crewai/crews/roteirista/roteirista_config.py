from typing import Dict, Any
from .agente_config import AgenteConfig
from ...models import GroqManager, LLMA3_8, MIXTRAL_8_7, LLMA3_1_70

def default_config() -> Dict[str, Any]:
    """
    Função que retorna a configuração padrão para o roteirista.

    Retorna:
        Dict[str, Any]: Um dicionário contendo 'max_rpm' e a lista 'agente_config'.
    """
    llm_manager = GroqManager(model_key=LLMA3_1_70)
    llm_instance = llm_manager.get_instance()
    
    return {        
        'agente_config': [AgenteConfig(model_name=llm_instance['model_name'], max_rpm=llm_instance['max_rpm']) for _ in range(3)]
    }

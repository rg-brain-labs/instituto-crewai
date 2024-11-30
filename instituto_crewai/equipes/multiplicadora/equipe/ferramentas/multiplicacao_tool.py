from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel
from typing import Any, Type

class MultiplicacaoToolSchema(BaseModel):
    primeiro_numero: int = "Primeiro número da multiplicação"
    segundo_numero: int = "Segundo número da multiplicação"

class MultiplicacaoTool(BaseTool):
    name: str = "Ferramenta de Multiplicação"
    description: str = "Útil para quando você precisa multiplicar dois números"
    args_schema: Type[BaseModel] = MultiplicacaoToolSchema

    def _run(self, **kwargs: Any) -> str:
        primeiro_numero = kwargs.get("primeiro_numero")
        segundo_numero = kwargs.get("segundo_numero")
        
        resultado = primeiro_numero * segundo_numero

        return ("O resultado da multiplicação é "
                f"{primeiro_numero} * {segundo_numero} = {resultado}")
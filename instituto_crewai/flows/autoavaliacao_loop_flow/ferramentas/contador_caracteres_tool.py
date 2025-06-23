from typing import Type

from crewai_tools import BaseTool
from pydantic import BaseModel, Field


class ContadorCaracteresToolInput(BaseModel):
    """Esquema de entrada para ContadorCaracteresTool."""

    texto: str = Field(..., description="O texto de entrada para contagem de caracteres.")


class ContadorCaracteresTool(BaseTool):
    name: str = "Contador Caracteres Tool"
    description: str = "Calcula o comprimento de uma sequência de caracteres."
    args_schema: Type[BaseModel] = ContadorCaracteresToolInput

    def _run(self, texto: str) -> str:
        contagem_caracteres = len(texto)
        return f"A cadeia de caracteres de entrada contém {contagem_caracteres} caracteres."
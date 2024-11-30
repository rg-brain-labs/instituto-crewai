from crewai.tools.base_tool import BaseTool

class MultiplicacaoTool(BaseTool):
    name: str = "Ferramenta de Multiplicação"
    description: str = "Útil para quando você precisa multiplicar dois números"

    def _run(self, primeiro_numero: int, segundo_numero: int) -> str:
        resultado = primeiro_numero * segundo_numero

        return f"""
            O resultado da multiplicação é 
            {primeiro_numero} * {segundo_numero} = {resultado}
        """
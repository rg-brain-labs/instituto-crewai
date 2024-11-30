from .equipe.multiplicadora_execucao import ExecucaoMultiplicadora
from rich.table import Table
from rich.console import Console

def main():
    resultado = ExecucaoMultiplicadora().executar()
    
    # Criando a tabela
    tabela_resultado = Table(show_header=False, title="[bold magenta]Resposta Equipe Multiplicadora[/bold magenta]")
    tabela_resultado.add_row(resultado.raw)
    tabela_resultado.add_row("")

    # Criando a tabela para o consumo de tokens
    tabela_tokens = Table(title="[bold magenta]Consumo de Tokens[/bold magenta]", show_header=True, header_style="bold cyan")
    tabela_tokens.add_column("Tipo", justify="left")
    tabela_tokens.add_column("Quantidade", justify="right")

    # Adicionando linhas para cada métrica de uso de tokens
    for chave, valor in resultado.token_usage:
        tabela_tokens.add_row(chave.replace("_", " ").capitalize(), str(valor))

    # Exibindo as tabelas no console
    console = Console()
    console.print("\n")
    console.print(tabela_resultado)
    console.print("\n")
    console.print(tabela_tokens)
    console.print("\n")

if __name__ == '__main__':
    main()
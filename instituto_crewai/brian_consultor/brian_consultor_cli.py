from .flow.brian_consultor_execucao import BrianConsultorExecucao
from rich.table import Table
from rich.console import Console

def main():

    tabela_introducao = Table(show_header=False, title="[bold magenta]BRIAN CONSULTOR[/bold magenta]")
    tabela_introducao.add_row("Bem-vindo ao Fantástico, Galáctico e Master Of Puppets of the Universe, [bold red]BRIAN CONSULTOR[/bold red] 🌌🎸✨\n")

    tabela_resultado = Table(show_header=False, title="[bold magenta]ANÁLISE FANTÁSTICA[/bold magenta]")
    avaliacao = BrianConsultorExecucao().executar_consultor_consorcio_flow()  
    tabela_resultado.add_row(avaliacao)

    console = Console()
    console.print(tabela_introducao)
    console.print("\n")
    console.print(tabela_resultado)

if __name__ == '__main__':
    main()
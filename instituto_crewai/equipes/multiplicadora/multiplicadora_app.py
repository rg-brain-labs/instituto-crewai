from .equipe.multiplicadora_execucao import ExecucaoMultiplicadora
from rich import print

def main():
    resultado = ExecucaoMultiplicadora().executar()
    print(resultado.raw)

if __name__ == '__main__':
    main()
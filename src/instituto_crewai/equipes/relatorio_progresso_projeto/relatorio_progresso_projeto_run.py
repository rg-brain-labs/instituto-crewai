import streamlit.web.cli as stcli
import sys
from dotenv import load_dotenv


def main():
    load_dotenv()   
    sys.argv = ["streamlit", "run", "src/instituto_crewai/equipes/relatorio_progresso_projeto/relatorio_progresso_projeto_app.py"]    
    stcli.main()

if __name__ == "__main__":
    main()
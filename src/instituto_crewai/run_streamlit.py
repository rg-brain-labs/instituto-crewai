import streamlit.web.cli as stcli
import sys

def main():
    sys.argv = ["streamlit", "run", "src/instituto_crewai/equipes/streamlit_equipes_template/streamlit_app.py"]    
    stcli.main()

if __name__ == "__main__":
    main()
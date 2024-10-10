import streamlit.web.cli as stcli
import sys

def main():
    sys.argv = ["streamlit", "run", "src/instituto_crewai/equipes/auto_doc/streamlit_app.py"]    
    stcli.main()

if __name__ == "__main__":
    main()
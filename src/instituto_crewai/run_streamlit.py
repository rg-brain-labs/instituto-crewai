import streamlit.web.cli as stcli
import sys

def main():
    sys.argv = ["streamlit", "run", "src/instituto_crewai/main_streamlit.py"]    
    stcli.main()

if __name__ == "__main__":
    main()
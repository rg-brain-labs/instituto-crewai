import sys, os
from dotenv import load_dotenv

def main():
    load_dotenv()   
    sys.argv = ["poetry", "run", "institulo_crewai/flow/autoavaliacao_loop_flow/autoavaliacao_loop_flow_main.py"]

if __name__ == "__main__":
    main()
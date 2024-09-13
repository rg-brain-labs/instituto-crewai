from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    dotenv_path = Path(__file__).parents[1] / 'config' / '.env'   
    load_dotenv(dotenv_path)
from crews.instragram_crew import InstagramCrew
from llms.llm_manager import LLMManager
from llms.gemini import GeminiModels

import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega variáveis de ambiente
dotenv_path = Path(__file__).parent / 'config' / '.env'
load_dotenv(dotenv_path)

def main():
    google_api_key = os.getenv("GOOGLE_API_KEY")
    llm_manager = LLMManager(api_key=google_api_key)
    llm = llm_manager.create_llm('gemini', GeminiModels.GEMINI_1_0_PRO)
    
    crew = InstagramCrew(llm=llm)
    
    crew.run()   

if __name__ == "__main__":
    main()

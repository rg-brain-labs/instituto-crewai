from crews import InstagramCrew
from datetime import datetime

def main():
    crew = InstagramCrew().crew()
    
    result = crew.kickoff(inputs={
      'topico':'Inteligência Artificial e Agentes Inteligêntes',
      'n':1})
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"posts-{current_date}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(result)   

if __name__ == "__main__":
    main()

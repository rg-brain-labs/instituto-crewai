from campanha_crew import CampanhaCrew
from datetime import datetime

def main():
    crew = CampanhaCrew().crew()

    inputs = {
        "lead_name": "AetherTech",
        "industry": "Research and Development of Advanced Energy Technologies",
        "key_decision_maker": "Dr. Eleanor Quinn",
        "position": "CEO",
        "milestone": "Launch of new space-based energy infrastructure"
    }
    
    result = crew.kickoff(inputs=inputs)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"campanha-{current_date}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(result)   

if __name__ == "__main__":
    main()
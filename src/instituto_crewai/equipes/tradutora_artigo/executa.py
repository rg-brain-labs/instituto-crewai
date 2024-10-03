from instituto_crewai.equipes.tradutora_artigo.equipe import TradutoraArtigo

def main():
    equipe = TradutoraArtigo("groq/llama-3.1-8b-instant", 35).crew()
    
    resultado = equipe.kickoff()
    print(resultado)
    
if __name__ == "__main__":
    main()
# Para executar poetry run streamlit run "src/instituto_crewai/equipes/streamlit_equipes_template/streamlit_app.py"
import streamlit as st

# Configuração da Página Principal
st.set_page_config(layout="wide", page_title="Automatizando Projetos", page_icon="🎬")
st.title("🤖📋💡 Automatizando Projetos")

# Iniciando Variáveis de sessão
def status_inicial():
    pass

status_inicial()

# Dessa forma evitamos o WARNING: Overriding of current TracerProvider is not allowed    
@st.cache_resource
def criar_automated_project_crew():
    pass

st.session_state.equipe = criar_automated_project_crew()

def main():
    # Sidebar       
    st.sidebar.info("Breve Descrição da equipe.") 
   
if __name__ == "__main__":
    main()
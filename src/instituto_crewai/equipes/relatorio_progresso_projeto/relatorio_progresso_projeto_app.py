# Para executar poetry run streamlit run .\src\instituto_crewai\equipes\automated_project\automatizando_projetos_app.py
import streamlit as st
from instituto_crewai.equipes.automated_project.equipe.automatizando_projetos_crew import AutomatizandoProjetosCrew

st.set_page_config(layout="wide", page_title="Automatizando Projetos", page_icon="🤖")
st.title("🤖📋💡 Automatizando Projetos")

# Iniciando Variáveis de sessão
def status_inicial():
    if 'mostrar_inputs' not in st.session_state:
        st.session_state.mostrar_inputs = True
    if 'projeto' not in st.session_state:
        st.session_state.projeto
    if 'industria' not in st.session_state:
        st.session_state.industria
    if 'objetivos_projeto' not in st.session_state:
        st.session_state.objetivos_projeto
    if 'membros_equipe' not in st.session_state:
        st.session_state.membros_equipe
    if 'requisitos_projeto' not in st.session_state:
        st.session_state.requisitos_projeto

status_inicial()

@st.cache_resource
def criar_automatizando_projetos_crew():
    return AutomatizandoProjetosCrew().crew()

st.session_state.equipe = criar_automatizando_projetos_crew()

def main():
    # Sidebar       
    st.sidebar.info("Automação de Projetos") 

    if st.session_state.mostrar_inputs:
        st.subheader("Entradas da Equipe")

        st.session_state.projeto = st.text_input(label="Tipo de Projeto", value="Website", key="projeto")
        st.session_state.industria = st.text_input(label="Indústria", value="Tecnologia", key="industria")
        # st.session_state.objetivos_projeto = st.text_area(label="Digite ou cole seu texto aqui", height=200, key="projeto")
        # st.session_state.membros_equipe = st.text_area(label="Digite ou cole seu texto aqui", height=200, key="projeto")
        # st.session_state.requisitos_projeto = st.text_area(label="Digite ou cole seu texto aqui", height=200, key="projeto")
   
if __name__ == "__main__":
    main()
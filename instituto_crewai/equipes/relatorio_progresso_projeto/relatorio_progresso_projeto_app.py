import streamlit as st
from instituto_crewai.equipes.relatorio_progresso_projeto.equipe.relatorio_progresso_projeto_crew import RelatorioProgressoProjetoCrew
#from agents import analyze_software_project, analyze_personal_project

st.set_page_config(
        page_title="📋 Projeto Progress Tracker", 
        page_icon="🤖", 
        layout="wide"
    )

def initialize_session_state():
    if 'board_selected' not in st.session_state:
        st.session_state.board_selected = None
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None

@st.cache_resource
def criar_equipe_progresso_projeto():
    return RelatorioProgressoProjetoCrew().crew()

st.session_state.progresso_projeto = criar_equipe_progresso_projeto()

def main():
    
    # Main title and description
    st.title("🤖 Projeto Progress Tracker")
    st.markdown("""
    ### Análise Inteligente do Seu Projeto
    Selecione o tipo de projeto e deixe nossos agentes inteligentes analisarem seu progresso!
    """)
    
    # Sidebar for board selection
    st.sidebar.header("🔍 Selecione seu Projeto")
    
    selected_board = st.sidebar.selectbox(
        "Escolha o Board do Trello", 
        ["Rumo ao Extraordinário", "Exemplo Progresso Projeto"]
    )   
    
    # Analyze button
    if st.sidebar.button("🚀 Analisar Progresso"):
        # Choose analysis function based on project type
        if selected_board == "Rumo ao Extraordinário":
            result = "analyze_software_project(selected_board) - Rumo ao Extraordinário"
        else:
            result = st.session_state.progresso_projeto.kickoff()
        
        # Store result in session state
        st.session_state.analysis_result = result
    
    # Display analysis result
    if st.session_state.analysis_result:
        st.markdown("### 📊 Resultado da Análise")
        st.markdown(st.session_state.analysis_result)

if __name__ == "__main__":
    initialize_session_state()
    main()
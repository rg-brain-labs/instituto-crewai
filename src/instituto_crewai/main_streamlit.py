import streamlit as st
from datetime import datetime, date
import json
from instituto_crewai.crews import RoteiristaController

# Inicialização do controlador e variáveis de sessão
controller = RoteiristaController()

# Config
st.set_page_config(layout="wide", page_title="Roteirizador", page_icon="🎬")

# Initial State
if 'texto_base' not in st.session_state:
    st.session_state['texto_base'] = ""
if 'texto_roteirizado' not in st.session_state:
    st.session_state['texto_roteirizado'] = ""
if 'token_usage' not in st.session_state:
    st.session_state['token_usage'] = None

def display_token_usage(token_usage):
    st.sidebar.subheader("Uso de Tokens")
    st.sidebar.metric(label="Total de Tokens", value=f"{token_usage.total_tokens:,}")
    st.sidebar.metric(label="Tokens do Prompt", value=f"{token_usage.prompt_tokens:,}")
    st.sidebar.metric(label="Tokens da Resposta", value=f"{token_usage.completion_tokens:,}")
    st.sidebar.metric(label="Requisições Bem-sucedidas", value=token_usage.successful_requests)

def main():
    # Sidebar
    st.sidebar.title("Roteirizador")
    st.sidebar.write("Bem-vindo(a) ao **Roteirizador**, a ferramenta que irá automatizar seu processo de criação de roteiros.")
    st.sidebar.divider()
    st.sidebar.info("Esta ferramenta transforma um texto base em um roteiro estruturado.")
    
    # Display Token Usage KPIs in sidebar
    if st.session_state.token_usage:
        st.sidebar.divider()
        display_token_usage(st.session_state.token_usage)

    # Main content
    st.title("Criar Roteiro")
    
    # Input area
    st.subheader("Texto Base")
    texto_base = st.text_area("Digite ou cole seu texto base aqui", height=200, key="input_text")
    st.write(f"Caracteres: {len(texto_base)}")

    # Process button
    if st.button("Roteirizar", type="primary"):
        with st.spinner("Processando..."):
            crew_result = controller.run({'texto_base': texto_base})
        st.session_state.texto_roteirizado = crew_result.raw
        st.session_state.token_usage = crew_result.token_usage
        #st.experimental_rerun()  # Rerun to update sidebar
    
    # Output area
    st.subheader("Roteiro Gerado")
    texto_roteirizado = st.text_area("Seu roteiro aparecerá aqui", value=st.session_state.texto_roteirizado, height=300, key="output_text")
    st.write(f"Caracteres: {len(texto_roteirizado)}")

    # Download button
    if st.session_state.texto_roteirizado:
        st.download_button(
            label="Baixar Roteiro",
            data=st.session_state.texto_roteirizado,
            file_name="roteiro_gerado.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
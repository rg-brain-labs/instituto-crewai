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
if 'historico' not in st.session_state:
    st.session_state['historico'] = []
if 'tasks_output' not in st.session_state:
    st.session_state['tasks_output'] = []
if 'show_input' not in st.session_state:
    st.session_state['show_input'] = True

def display_token_usage(token_usage):
    st.sidebar.subheader("Uso de Tokens")
    st.sidebar.metric(label="Total de Tokens", value=f"{token_usage.total_tokens:,}")
    st.sidebar.metric(label="Tokens do Prompt", value=f"{token_usage.prompt_tokens:,}")
    st.sidebar.metric(label="Tokens da Resposta", value=f"{token_usage.completion_tokens:,}")
    st.sidebar.metric(label="Requisições Bem-sucedidas", value=token_usage.successful_requests)

def analisar_texto(texto):
    palavras = texto.split()
    return {
        "num_palavras": len(palavras),
        "tempo_leitura": len(palavras) // 200  # Assumindo uma velocidade média de leitura de 200 palavras por minuto
    }

def main():
    # Sidebar
    st.sidebar.title("Roteirizador")
    st.sidebar.write("Bem-vindo(a) ao **Roteirizador**, a ferramenta que irá automatizar seu processo de criação de roteiros.")
    st.sidebar.divider()
    st.sidebar.info("Esta ferramenta transforma um texto base em um roteiro estruturado.")
   
    # Opções de personalização
    estilo_roteiro = st.sidebar.selectbox("Estilo do Roteiro", ["Padrão", "Cinema", "Teatro", "TV"])
    tom_roteiro = st.sidebar.slider("Tom do Roteiro", 1, 5, 3, help="1: Muito sério, 5: Muito descontraído")

    # Display Token Usage KPIs in sidebar
    if st.session_state.token_usage:
        st.sidebar.divider()
        display_token_usage(st.session_state.token_usage)

    # Main content
    st.title("Criar Roteiro")
   
    # Input area
    if st.session_state.show_input:
        st.subheader("Texto Base")
        texto_base = st.text_area("Digite ou cole seu texto base aqui", height=200, key="input_text")
        analise_base = analisar_texto(texto_base)
        st.write(f"Caracteres: {len(texto_base)} | Palavras: {analise_base['num_palavras']}")

        # Process button
        if st.button("Roteirizar", type="primary"):           
            with st.spinner("Processando..."):
                crew_result = controller.run({
                    'texto_base': texto_base,
                    #'estilo': estilo_roteiro,
                    #'tom': tom_roteiro
                })
            st.session_state.texto_roteirizado = crew_result.raw
            st.session_state.token_usage = crew_result.token_usage
            st.session_state.tasks_output = crew_result.tasks_output
            st.session_state.historico.append({
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "texto_base": texto_base,
                "roteiro": crew_result.raw,
                "tasks_output": crew_result.tasks_output
            })
            st.session_state.show_input = False
            st.rerun()  # Rerun to update sidebar
    else:
        if st.button("Novo Roteiro"):
            st.session_state.show_input = True
            st.rerun()

    # Output area
    if not st.session_state.show_input and st.session_state.tasks_output:
        st.subheader("Resultados das Tarefas")
        
        # Criar tabs para cada tarefa
        task_names = [task.name for task in st.session_state.tasks_output]
        tabs = st.tabs(task_names)
        
        for i, tab in enumerate(tabs):
            with tab:
                task = st.session_state.tasks_output[i]
                st.write(f"**Descrição:** {task.description}")
                st.write(f"**Agente:** {task.agent}")
                st.write(f"**Resumo:** {task.summary}")
                st.text_area("Resultado", value=task.raw, height=300, key=f"task_output_{i}")

        st.subheader("Roteiro Final")
        texto_roteirizado = st.text_area("Roteiro gerado", value=st.session_state.texto_roteirizado, height=300, key="output_text")
        analise_roteiro = analisar_texto(texto_roteirizado)
        st.write(f"Caracteres: {len(texto_roteirizado)} | Palavras: {analise_roteiro['num_palavras']} | Tempo estimado de leitura: {analise_roteiro['tempo_leitura']} minutos")

        # Download button
        if st.session_state.texto_roteirizado:
            st.download_button(
                label="Baixar Roteiro",
                data=st.session_state.texto_roteirizado,
                file_name=f"roteiro_gerado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

    # Histórico
    if st.session_state.historico:
        st.subheader("Histórico de Roteiros")
        for i, item in enumerate(reversed(st.session_state.historico)):
            with st.expander(f"Roteiro {len(st.session_state.historico) - i}: {item['data']}"):
                st.text_area("Texto Base", item['texto_base'], height=100)
                st.text_area("Roteiro Gerado", item['roteiro'], height=200)
                if 'tasks_output' in item:
                    st.subheader("Resultados das Tarefas")
                    for task in item['tasks_output']:
                        st.write(f"**Tarefa:** {task.name}")
                        st.write(f"**Agente:** {task.agent}")
                        st.text_area("Resultado", value=task.raw, height=150)

if __name__ == "__main__":
    main()
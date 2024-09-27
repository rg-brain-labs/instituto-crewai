import streamlit as st
from datetime import datetime
from instituto_crewai.crews import RoteiristaController

# Inicialização do controlador e variáveis de sessão
controller = RoteiristaController()

# Config
st.set_page_config(layout="wide", page_title="Roteirizador", page_icon="🎬")

# Definição dos modelos e seus custos
MODELOS = {
    "gpt-4o-2024-08-06": {"prompt": 2.50, "completion": 10.00},
    "GPT-4o mini": {"prompt": 0.15, "completion": 0.60},
    "o1-preview": {"prompt": 15.00, "completion": 60.00},
    "o1-mini": {"prompt": 3.00, "completion": 12.00},
    "gemini-1.5-flash": {"prompt": 0.15, "completion": 0.60},
    "gemini-1.5-pro": {"prompt": 7.00, "completion": 21.00},
    "gemini-1.0-pro": {"prompt": 0.50, "completion": 1.50},
    "grog-Llama 3.1 70B": {"prompt": 0.59, "completion": 0.79},
    "groq-Llama 3.1 8B": {"prompt": 0.05, "completion": 0.08},
}

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
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = 0
if 'total_prompt_tokens' not in st.session_state:
    st.session_state['total_prompt_tokens'] = 0
if 'total_completion_tokens' not in st.session_state:
    st.session_state['total_completion_tokens'] = 0
if 'total_successful_requests' not in st.session_state:
    st.session_state['total_successful_requests'] = 0
if 'modelo_selecionado' not in st.session_state:
    st.session_state['modelo_selecionado'] = "GPT-4o mini"

def calcular_custo(prompt_tokens, completion_tokens, modelo):
    custo_prompt = (prompt_tokens / 1_000_000) * MODELOS[modelo]["prompt"]
    custo_completion = (completion_tokens / 1_000_000) * MODELOS[modelo]["completion"]
    return custo_prompt + custo_completion

def display_token_usage():
    modelo = st.session_state.modelo_selecionado
    custo_total = calcular_custo(st.session_state.total_prompt_tokens, st.session_state.total_completion_tokens, modelo)
    
    st.sidebar.subheader("Uso de Tokens (Acumulado)")
    st.sidebar.metric("Requisições Bem-sucedidas", st.session_state.total_successful_requests)
    
    col1_token, col2_token = st.sidebar.columns(2)
    col1_token.metric(label="Tokens do Prompt", value=f"{st.session_state.total_prompt_tokens:,}")
    col2_token.metric(label="Tokens da Resposta", value=f"{st.session_state.total_completion_tokens:,}")
    
    col1_total, col2_total = st.sidebar.columns(2)
    col1_total.metric(label="Total de Tokens", value=f"{st.session_state.total_tokens:,}")
    col2_total.metric("Custo Estimado", f"${custo_total:.4f}")
    

def analisar_texto(texto):
    palavras = texto.split()
    return {
        "num_palavras": len(palavras),
        "tempo_leitura": len(palavras) // 200  # Assumindo uma velocidade média de leitura de 200 palavras por minuto
    }

def main():
    # Sidebar
    st.sidebar.title("Roteirizador")    
    st.sidebar.info("Esta ferramenta transforma um texto base em um roteiro estruturado.")   
    
    # Seleção do modelo
    st.session_state.modelo_selecionado = st.sidebar.selectbox(
        "Selecione o modelo",
        options=list(MODELOS.keys()),
        index=list(MODELOS.keys()).index(st.session_state.modelo_selecionado)
    )
    
    # Display Token Usage KPIs in sidebar
    display_token_usage()

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
                })
            st.session_state.texto_roteirizado = crew_result.raw
            st.session_state.token_usage = crew_result.token_usage
            st.session_state.tasks_output = crew_result.tasks_output
            
            # Atualizar tokens acumulados
            st.session_state.total_tokens += crew_result.token_usage.total_tokens
            st.session_state.total_prompt_tokens += crew_result.token_usage.prompt_tokens
            st.session_state.total_completion_tokens += crew_result.token_usage.completion_tokens
            st.session_state.total_successful_requests += crew_result.token_usage.successful_requests
            
            st.session_state.historico.append({
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "texto_base": texto_base,
                "roteiro": crew_result.raw,
                "tasks_output": crew_result.tasks_output,
                "token_usage": {
                    "total_tokens": crew_result.token_usage.total_tokens,
                    "prompt_tokens": crew_result.token_usage.prompt_tokens,
                    "completion_tokens": crew_result.token_usage.completion_tokens,
                    "successful_requests": crew_result.token_usage.successful_requests
                },
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
        task_agent = [task.agent for task in st.session_state.tasks_output]
        tabs = st.tabs(task_agent)
        
        for i, tab in enumerate(tabs):
            with tab:
                task = st.session_state.tasks_output[i]
                st.write(f"**Resumo:** {task.summary}")
                st.text_area("Resultado", value=task.raw, height=300, key=f"task_output_{i}")

        st.divider()
        
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
                st.text_area("Texto Base", item['texto_base'], height=100, disabled=True)
                st.text_area("Roteiro Gerado", item['roteiro'], height=200)               
                st.write("**Uso de Tokens:**")
                col1, col2, col3 = st.columns(3)
                col1.metric("Total", f"{item['token_usage']['total_tokens']:,}")
                col2.metric("Prompt", f"{item['token_usage']['prompt_tokens']:,}")
                col3.metric("Resposta", f"{item['token_usage']['completion_tokens']:,}")
                st.write(f"Requisições bem-sucedidas: {item['token_usage']['successful_requests']}")
                custo_estimado = calcular_custo(item['token_usage']['prompt_tokens'], item['token_usage']['completion_tokens'], st.session_state.modelo_selecionado)
                st.write(f"**Custo Estimado:** ${custo_estimado:.4f}")
                st.divider()
                if 'tasks_output' in item:
                    st.subheader("Resultados das Tarefas")
                    for task in item['tasks_output']:
                        st.write(f"**Agente:** {task.agent}")
                        st.write(f"**Tarefa:** {task.name}")
                        st.text_area("Resultado", value=task.raw, height=150, disabled=True)                       
                   

if __name__ == "__main__":
    main()
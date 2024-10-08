import streamlit as st
from PIL import Image
from datetime import datetime

# Configuração da Página Principal
st.set_page_config(layout="wide", page_title="Nome Projeto", page_icon="🎬")
st.title("🎥 Nome Projeto")


# Iniciando Variáveis de sessão
def status_inicial():
    if 'texto_base' not in st.session_state:
        st.session_state.texto_base = ""  
    if 'mostrar_inputs' not in st.session_state:
        st.session_state.mostrar_inputs = True

status_inicial()

def analisar_texto():
    palavras = st.session_state.texto_base.split()
    return {
        "num_palavras": len(palavras),
        "tempo_leitura": len(palavras) // 200  # Assumindo uma velocidade média de leitura de 200 palavras por minuto
    }
    
# Dessa forma evitamos o erro WARNING: Overriding of current TracerProvider is not allowed    
@st.cache_resource
def criar_equipe():
    return None

st.session_state.equipe = criar_equipe()

def main():
    # Sidebar       
    st.sidebar.info("Breve Descrição da equipe.") 
   
    # Condiguração Roteirizador
    if st.session_state.mostrar_inputs:
        st.subheader("Entradas da Equipe")
        
        # Add a selectbox for choosing predefined examples
        example_options = ["Escreva seu próprio texto"] + [example['titulo'] for example in texto_base_examples['exemplos']]
        selected_example = st.selectbox("Escolha um exemplo ou escreva seu próprio texto", options=example_options)
        
        if selected_example == "Escreva seu próprio texto":
            st.session_state.texto_base = st.text_area(label="Digite ou cole seu texto aqui", height=200, key="input_text")
        else:
            selected_text = next(example['texto'] for example in texto_base_examples['exemplos'] if example['titulo'] == selected_example)
            st.session_state.texto_base = st.text_area(label="Digite ou cole seu texto aqui", value=selected_text, height=200, key="input_text")
        
        analise_base = analisar_texto()
        st.write(f"Caracteres: {len(st.session_state.texto_base)} | Palavras: {analise_base['num_palavras']}")

        # Process button
        if st.button("Trabalhar", type="primary"):
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
        if st.button("Novo Roteiro", icon="🧪"):
            st.session_state.show_input = True
            st.rerun()

    if not st.session_state.show_input and st.session_state.tasks_output:
        # Resultados Roteirizador
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
                icon="🪄",
                data=st.session_state.texto_roteirizado,
                file_name=f"roteiro_gerado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

        st.divider()

        # Gasto de Tokens   
        # Seleção do modelo
        st.subheader("Uso de Tokens (Acumulado)")
        st.session_state.modelo_selecionado = st.selectbox(
            "Selecione o modelo para calcular custo",
            options=list(MODELOS.keys()),
        )
        
        # Display Token Usage KPIs in sidebar
        display_token_usage()
        
        st.divider()

    # Histórico
    if st.session_state.historico:
        st.subheader("Histórico de Roteiros")
        for i, item in enumerate(reversed(st.session_state.historico)):
            with st.expander(f"Roteiro {len(st.session_state.historico) - i}: {item['data']}"):
                st.text_area("Texto Base", item['texto_base'], height=100, disabled=True, key=f"texto-base-{i}")
                st.text_area("Roteiro Gerado", item['roteiro'], height=200, key=f"roteiro-gerado-{i}")               
                st.write("**Uso de Tokens:**")
                col1, col2, col3 = st.columns(3)
                col1.metric("Total", f"{item['token_usage']['total_tokens']:,}")
                col2.metric("Prompt", f"{item['token_usage']['prompt_tokens']:,}")
                col3.metric("Resposta", f"{item['token_usage']['completion_tokens']:,}")
                st.write(f"Requisições bem-sucedidas: {item['token_usage']['successful_requests']}")                
                st.divider()
                if 'tasks_output' in item:
                    st.subheader("Resultados das Tarefas")
                    for task in item['tasks_output']:
                        st.write(f"**Agente:** {task.agent}")
                        st.write(f"**Tarefa:** {task.name}")
                        st.text_area("Resultado", value=task.raw, height=150, disabled=True, key=f"resultado-{i}-{task.agent}")                       
                   

if __name__ == "__main__":
    main()

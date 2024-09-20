import streamlit as st
from datetime import datetime, date
import json
from .crews import RoteiristController

# Inicialização do controlador e variáveis de sessão
controller = RoteiristController()

if 'roteiros' not in st.session_state:
    st.session_state.roteiros = []
if 'roteiros_hoje' not in st.session_state:
    st.session_state.roteiros_hoje = 0
if 'ultima_data' not in st.session_state:
    st.session_state.ultima_data = date.today()

# Função para salvar roteiros
def salvar_roteiro(roteiro):
    if len(st.session_state.roteiros) >= 3:
        st.session_state.roteiros.pop(0)
    st.session_state.roteiros.append(roteiro)

# Função para verificar e atualizar o limite diário
def verificar_limite_diario():
    hoje = date.today()
    if hoje != st.session_state.ultima_data:
        st.session_state.roteiros_hoje = 0
        st.session_state.ultima_data = hoje
    return st.session_state.roteiros_hoje < 3

# Interface principal
st.title("Gerador de Roteiros")

# Seleção de modo
modo = st.radio("Escolha o modo de criação:", ("Com texto inicial", "Sem texto inicial"))

if modo == "Com texto inicial":
    texto_inicial = st.text_area("Digite o texto inicial para o roteiro:")
else:
    tema = st.text_input("Digite o tema ou objetivo do roteiro:")

# Seleção de estilo
estilo = st.selectbox("Escolha o estilo do roteiro:", 
                      ["Vídeo para YouTube", "Conversa entre dois personagens", "TED Talk"])

# Seleção de tom e emoção (para conversa entre personagens)
if estilo == "Conversa entre dois personagens":
    tom = st.selectbox("Escolha o tom da conversa:", 
                       ["Formal", "Descontraído", "Cômico", "Profissional", "Motivacional"])
    emocao = st.selectbox("Escolha a emoção predominante:", 
                          ["Empatia", "Raiva", "Alegria", "Tristeza", "Sarcasmo", "Seriedade"])

# Área de descrição adicional
st.subheader("Descrição Adicional")
ambiente = st.text_input("Ambiente:")
tema_adicional = st.text_input("Tema adicional:")
personagens = st.text_input("Personagens:")
objetivo = st.text_input("Objetivo:")

# Estrutura do roteiro
st.subheader("Estrutura do Roteiro")
estrutura = {
    "Introdução": st.text_area("Introdução:"),
    "Desenvolvimento": st.text_area("Desenvolvimento:"),
    "Clímax": st.text_area("Clímax:"),
    "Conclusão": st.text_area("Conclusão:")
}

# Botão para gerar roteiro
if st.button("Gerar Roteiro"):
    if verificar_limite_diario():
        # Aqui você chamaria a função do controller para gerar o roteiro
        # Por enquanto, vamos simular a geração
        roteiro_gerado = f"Roteiro gerado para {estilo}\n\n"
        for secao, conteudo in estrutura.items():
            roteiro_gerado += f"{secao}:\n{conteudo}\n\n"
        
        st.text_area("Roteiro Gerado:", roteiro_gerado, height=300)
        
        if st.button("Salvar Roteiro"):
            salvar_roteiro(roteiro_gerado)
            st.session_state.roteiros_hoje += 1
            st.success("Roteiro salvo com sucesso!")
    else:
        st.warning("Você atingiu o limite diário de 3 roteiros. Tente editar roteiros existentes.")

# Exibição do histórico
st.subheader("Histórico de Roteiros")
for i, roteiro in enumerate(st.session_state.roteiros):
    st.text_area(f"Roteiro {i+1}", roteiro, height=150)

if len(st.session_state.roteiros) == 3:
    st.info("O histórico está cheio. O próximo roteiro substituirá o mais antigo.")

# Área de demonstração
st.sidebar.title("Demonstração")
st.sidebar.info("""
Dicas para usar o app:
1. Escolha entre criar com ou sem texto inicial.
2. Selecione o estilo de roteiro desejado.
3. Preencha as informações adicionais para contextualizar melhor.
4. Use a estrutura sugerida ou personalize-a.
5. Clique em 'Gerar Roteiro' e depois em 'Salvar Roteiro' se desejar guardá-lo.
""")

# Exemplo de uso
st.sidebar.subheader("Exemplo de Uso")
st.sidebar.write("""
Tema: Inteligência Artificial no cotidiano
Estilo: TED Talk
Estrutura:
- Introdução: Apresente o conceito de IA
- Desenvolvimento: Exemplos de IA no dia a dia
- Clímax: Impactos futuros da IA
- Conclusão: Chamada para ação sobre o uso ético da IA
""")

# Contagem de roteiros restantes
roteiros_restantes = 3 - st.session_state.roteiros_hoje
st.sidebar.metric("Roteiros restantes hoje", roteiros_restantes)
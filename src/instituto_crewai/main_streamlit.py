import streamlit as st
from datetime import datetime, date
import json
from instituto_crewai.crews import RoteiristController

# Inicialização do controlador e variáveis de sessão
controller = RoteiristController()

# Config
st.set_page_config(layout="wide", page_title="Automatize-Me")

# Initial State
def initial_state():
    if 'texto_base' not in st.session_state:
        st.session_state['texto_base'] = None
    if 'processar' not in st.session_state:
        st.session_state['processar'] = None

initial_state()

# New Line
def new_line(n=1):
    for i in range(n):
        st.write("\n")
        
# Logo 
col1, col2, col3 = st.columns([0.25,1,0.25])
#col2.image("./assets/logo.png", use_column_width=True)
new_line(2)

# Description
with st.sidebar:    
    st.markdown("""
        # Roteirizador
        
        Bem Vindo(a) ao **Roteirizador**, a feramenta que irá lhe automatizar.    
    """, unsafe_allow_html=True)
    st.divider()

# Dataframe selection
st.markdown("<h2 align='center'> <b> Criar Roteiro", unsafe_allow_html=True)
new_line(1)

col1, col2 = st.columns(2 ,gap='small')

with col1:
    st.session_state.texto_base = st.text_area("Texto Base")
    _, _, col_btn = st.columns(3 ,gap='small')    
    with col_btn:
        st.session_state.processar = st.button("Roteirizar", use_container_width=True)
    
with col2:
    if(st.session_state.processar):
        st.text_area("Texto Roteirizado", value="Meu Mundo")
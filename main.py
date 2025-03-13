'''
Arquivo principal do projeto, onde é feito o controle de páginas e sessões.
Uma vez selecionada a página, o código chama a função correspondente.
'''

from src.page import page, upload, pacientes, resultados
import os
import streamlit as st
import yaml

st.set_page_config(page_title='Ajudante de diagnósticos', page_icon='🩺', layout='wide', initial_sidebar_state='expanded')


st.sidebar.subheader('Seleção de páginas')

pages = st.sidebar.radio('Selecione a página', ['Página inicial', 'Envio de documentos', "Resultados", 'Pacientes'])

if 'pacientes' not in st.session_state:
    with open('db/db.yaml', 'r', encoding='utf-8') as f:
        pacientes_lista = yaml.safe_load(f)
    st.session_state.pacientes = pacientes_lista

#Página inicial para colocar a documentação do projeto
if pages == 'Página Inicial':
    page()
#Página para envio de documentos dos exames
elif pages == 'Envio de documentos':
    upload()
#Página para visualização dos pacientes cadastrados
elif pages == 'Pacientes':
    pacientes()
#Página para visualização dos resultados do último exame anexado
elif pages == 'Resultados':
    resultados()
else:
    st.write("Selecione uma página no menu lateral")



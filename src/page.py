'''
Arquivo com as funções que definem as páginas do sistema.
'''

import streamlit as st
from PIL import Image
import os
import time
import yaml

#Página inicial
#TODO - Adicionar documentação do projeto
def page():
    st.text("texto")

#Página para envio de documentos dos exames
#TODO - Hoje apenas salva a imagem na raiz, para o protótipo final deve-se adicionar manejo das imagens
def upload():
    st.title("Envio de documentos")
    st.text("Envie imagem de tumografia de paciente")
    st.divider()
    uploaded_file = st.file_uploader("Escolha um arquivo")
    if uploaded_file is not None:
        st.image(uploaded_file)
    analise = st.button("Enviar para análise")
    if analise:
        if uploaded_file is None:
            st.error("Nenhum arquivo enviado. Por favor, envie um arquivo para análise.")
        else:
            with open('analise.png', 'wb') as f:
                f.write(uploaded_file.getvalue())
            with open('text.txt', 'w') as f:
                f.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.05)
                progress_bar.progress(i + 1)
            st.text("Análise concluída com sucesso! Consulte os resultados na aba de resultados.")

#Página para visualização dos resultados do último exame anexado
#TODO - Implementar a análise dos documentos ou uma documentação de teste para apresentar. Hoje fornece um diagnóstico aleatório
def resultados():
    st.title("Resultados da amostra")
    st.text("Aqui estão disponíveis os resultados da análise dos documentos enviados.")
    st.divider()
    if os.path.exists('analise.png'):

        import random as rd
        pct = rd.randint(0, 100)
        if pct < 30:
            color = 'green'
            icon = '🟢'
        elif pct > 70:
            color = 'red'
            icon = '🚨'
        else:
            color = 'orange'
            icon  = '⚠️'
        
        col1, col2 = st.columns(2)
        with col1:
            image = Image.open('analise.png')
            width, height = image.size
            st.image(image)
        with col2:
            st.subheader("Chance de diagnóstico de tumor maligno")
            st.write(f"<h1 style='color:{color}; font-size:{50}px;'>{pct} % {icon} </h1>", unsafe_allow_html=True)
            with open('text.txt', 'r') as f:
                texto = f.read()
            exp = st.expander("Descrição do diagnóstico")
            exp.write(texto)
            exp.button("Áudio descrição")

        st.divider()
        st.subheader("Salvar diagnóstico para paciente")

        nomes_pacientes = [paciente['nome'] for paciente in st.session_state.pacientes]
        paciente_alterar = st.selectbox("Nome do paciente", nomes_pacientes)
        observaçoes_alterar = st.text_area("Observações", height=200)

        if st.button("Salvar diagnóstico"):
            for paciente in st.session_state.pacientes:
                if paciente['nome'] == paciente_alterar:
                    if 'resultados' not in paciente.keys():
                        paciente['resultados'] = []
                    paciente['resultados'].append({'data': time.strftime("%d/%m/%Y %H:%M:%S"), 'observações': observaçoes_alterar, 'imagem': Image.open('analise.png')})
                    pacientes_data= [{k: v for k, v in paciente.items() 
                                                              if k != 'expander'} 
                                                              for paciente in st.session_state.pacientes]
                    with open('db/db.yaml', 'w', encoding='utf-8') as f:
                        yaml.dump(pacientes_data, f)
                    break
    else:
        st.text("Nenhum documento enviado. Adicione a imagem do exame na aba de envio de documentos.")

#Página para visualização dos pacientes cadastrados
#TODO - Adicionar mais informações de pacientes e a possibilidade de alterar os dados + seleção dos médicos.
def pacientes():
    st.title("Pacientes cadastrados")
    st.text("Aqui estão listados os pacientes cadastrados no sistema.")
    st.divider()

    for paciente in st.session_state.pacientes:
        paciente['expander'] = st.expander(f"{paciente['nome']}")
        paciente['expander'].write(f"Nome: {paciente['nome']}")
        paciente['expander'].write(f"Sexo: {paciente['sexo']}")
        paciente['expander'].write(f"Data de nascimento: {paciente['dt_nascimento']}")
        if 'resultados' in paciente.keys():
            paciente['expander'].write("Resultados:")
            for resultado in paciente['resultados']:
                paciente['expander'].write(f"Data: {resultado['data']}")
                paciente['expander'].write(f"Observações: {resultado['observações']}")
                paciente['expander'].image(resultado['imagem'])

#TODO - página de cadastro
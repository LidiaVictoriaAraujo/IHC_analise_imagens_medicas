import streamlit as st
import time
import datetime
from PIL import Image
from streamlit_option_menu import option_menu

# ========== CONFIG GERAL ==========
st.set_page_config(page_title="MediVisão", page_icon="🧬", layout="wide")

st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300..700&family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');
       
    .main {
        background-color: #FAF6EF;
        font-family: 'Quicksand', 'Segoe UI', sans-serif;
        font-optical-sizing: auto;
        font-weight: <weight>;
        font-style: normal;
        font-size: "18px"
    }

    html, body, [class*="css"] {
        font-family: 'Quicksand', 'Segoe UI', sans-serif;
        font-optical-sizing: auto;
        font-weight: <weight>;
        font-style: normal;
    }

    [data-testid="stSidebar"] {
        background-color: #7DA584;
    }

    h1, h2, h3 {
        color: #214c38;
        font-family: 'Quicksand', 'Segoe UI', sans-serif;
        color: #7DA584;
        font-optical-sizing: auto;
        font-weight: <weight>;
        font-style: normal;
    }

    .stButton > button {
        background-color: #7DA584;
        color: white;
        border-radius: 6px;
    }

    .stButton > button:hover {
        background-color: #3b8e68;
        border-color: white;
        color: white;    
    }
    </style>
""", unsafe_allow_html=True)

# Dados simulados de pacientes vinculados ao médico
if "pacientes" not in st.session_state:
    st.session_state.pacientes = {
        "joao_batista": {
            "nome": "João Batista Fernandes",
            "foto": "assets/persona-paciente.png",
            "idade": 67,
            "condicao": "Hipertensão, Diabetes",
            "analises": [],
            "resultados": [],
            "prontuario": []
        },
        "maria_alves": {
            "nome": "Maria Alves",
            "foto": "sem foto",
            "idade": 53,
            "condicao": "Pós-cirurgia abdominal",
            "analises": [],
            "resultados": [],
            "prontuario": []
        },
        "carlos_nunes": {
            "nome": "Carlos Nunes",
            "foto": "sem foto",
            "idade": 71,
            "condicao": "Exame de Rotina",
            "analises": [],
            "resultados": [],
            "prontuario": []
        }
    }

# ========== USUÁRIOS ==========
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        "medico": {"senha": "111", "perfil": "médico"},
        "enfermeiro": {"senha": "111", "perfil": "enfermeiro"},
        "paciente": {"senha": "111", "perfil": "paciente"},
        "admin": {"senha": "111", "perfil": "administrador"},
    }

# ========== AUTENTICAÇÃO ==========
def autenticar_usuario(username, senha):
    users = st.session_state.usuarios
    if username in users and users[username]["senha"] == senha:
        return users[username]["perfil"]
    return None

# ========== LOGIN ==========
def login_page():
    st.image("assets/logo.png", width=600)
    st.subheader("Sistema Inteligente de Diagnóstico Médico por IA")

    with st.form("login_form"):
        username = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            perfil = autenticar_usuario(username, senha)
            if perfil:
                st.session_state['autenticado'] = True
                st.session_state['usuario'] = username
                st.session_state['perfil'] = perfil
                st.query_params["pagina"] = "inicio"
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    st.markdown("Ainda não tem cadastro?")
    if st.button("Cadastrar novo usuário"):
        st.query_params["pagina"] = "cadastro"
        st.rerun()

# ========== CADASTRO ==========
def cadastro_page():
    st.image("assets/logo.png", width=120)
    st.title("Cadastro de Novo Usuário")
    st.markdown("Preencha os dados abaixo para criar sua conta.")

    with st.form("cadastro_form"):
        novo_usuario = st.text_input("Nome de usuário")
        nova_senha = st.text_input("Senha", type="password")
        perfil = st.selectbox("Perfil", ["médico", "paciente", "enfermeiro", "técnico-administrativo"])
        cadastrar = st.form_submit_button("Cadastrar")

        if cadastrar:
            if novo_usuario in st.session_state.usuarios:
                st.error("Nome de usuário já existe.")
            else:
                st.session_state.usuarios[novo_usuario] = {"senha": nova_senha, "perfil": perfil}
                st.success("Usuário cadastrado com sucesso! Faça login.")
                st.query_params["pagina"] = "login"
                st.rerun()

    if st.button("Voltar ao login"):
        st.query_params["pagina"] = "login"
        st.rerun()

# ========== PÁGINAS ==========
def pagina_inicio():
    st.title("Início")
    st.markdown("Bem-vindo ao **MediVisão**, sua plataforma de apoio ao diagnóstico por imagem.")
    st.info(f"Usuário logado: **{st.session_state['usuario']}** ({st.session_state['perfil']})")
    st.image("assets/drawing.png")
    
def pagina_lista_pacientes():
    st.title("Pacientes Acompanhados")
    pacientes = st.session_state.pacientes

    for pid, dados in pacientes.items():
        with st.expander(f"{dados['nome']} ({dados['idade']} anos)"):
            st.write(f"🩺 Condições clínicas: {dados['condicao']}")
            if st.button(f"Acessar {dados['nome']}", key=f"btn_{pid}"):
                st.query_params.clear()
                st.query_params.update({"pagina": "area_do_paciente", "paciente_id": pid})
                st.info("Acesse **Área do Paciente** no menu ao lado esquerdo!")
                

def menu_area_paciente(paciente_id):
    dados = st.session_state.pacientes[paciente_id]

    with st.sidebar:
        submenu = option_menu(
                f"{dados['nome']}",
                ["Dados Gerais", "Análise de Imagens", "Resultado da Análise", "Prontuário Médico", "Voltar"],
                icons=["person", "upload", "image", "clipboard", "arrow-left"],
                default_index=0,
                styles={
                    "container": {"background-color": "white", "padding": "30px"},
                    "icon": {"color": "#214c38", "font-size": "18px"},
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "--hover-color": "#a8d7c0"},
                    "nav-link-selected": {"background-color": "#7DA584", "color": "white"},
                }
            )
    
    return submenu

def pagina_area_do_paciente():
    st.title("Área do Paciente")
    paciente_id = st.query_params.get("paciente_id")
    pacientes = st.session_state.pacientes
    dados = st.session_state.pacientes[paciente_id]
    st.info(f"**{dados['nome']}**")
    
    if not paciente_id or paciente_id not in pacientes:
        st.error("Paciente não encontrado.")
        return
    
    paciente = pacientes[paciente_id]
    submenu_paciente(paciente_id, paciente)

def submenu_paciente(paciente_id, paciente):
    submenu = menu_area_paciente(paciente_id)

    if submenu == "Dados Gerais":
        st.title("Dados do Paciente")
        st.write(f"Nome: {paciente['nome']}")
        st.write(f"Idade: {paciente['idade']}")
        st.write(f"Condições: {paciente['condicao']}")

    elif submenu == "Análise de Imagens":
        st.title(f"Análise de Imagens")
        st.write(f"Nome: {paciente['nome']}")
        imagem = st.file_uploader("Enviar imagem de exame", type=["jpg", "jpeg", "png"])
        if imagem:
            paciente["analises"].append(imagem)
            st.image(imagem, caption="Imagem enviada", use_column_width=True)
            st.success("Imagem vinculada ao paciente.")

    elif submenu == "Resultado da Análise":
        st.title(f"Resultado da Análise")
        st.write(f"Nome: {paciente['nome']}")
        st.warning("⚠️ 80% de chance de detecção de anomalia.")
        st.image("assets/analise.png", caption="Imagem segmentada", use_column_width=True)
        st.audio("assets/resultado_analise_audio.mp3")
        paciente["resultados"].append("Resultado automático registrado.")
        st.success("Resultado registrado.")

    elif submenu == "Prontuário Médico":
        st.title(f"Prontuário Médico")
        st.write(f"Nome: {paciente['nome']}")
        prontuario = paciente["prontuario"]

        for item in reversed(prontuario):
            with st.expander(f"{item['data']} - {item['autor']}"):
                st.markdown(item["texto"])

        if st.button("✍️ Nova Anotação"):
            st.session_state["mostrar_form"] = True

        if st.session_state.get("mostrar_form", False):
            with st.form("form_prontuario"):
                texto = st.text_area("Evolução clínica", height=150)
                if st.form_submit_button("Salvar"):
                    if texto.strip():
                        anotacao = {
                            "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "autor": f"{st.session_state['usuario']} ({st.session_state['perfil']})",
                            "texto": texto
                        }
                        prontuario.append(anotacao)
                        st.success("Anotação registrada.")
                        st.session_state["mostrar_form"] = False
                        st.rerun()

    elif submenu == "Voltar":
        pagina_inicio()
        st.rerun()

def pagina_dados_pessoais():
    st.title("Dados Pessoais")
    
    usuario = st.session_state.get("usuario", "usuário")
    perfil = st.session_state.get("perfil", "indefinido")

    st.write(f"Usuário: `{usuario}`")
    st.write(f"Perfil: `{perfil}`")

    if perfil == "médico":
        st.image("assets/persona-medica.png", caption="Usuário")
        st.write("Nome completo: Helena Cavalcante Santos")
        st.write("Especialidade: Clínica Geral")
        st.write("CRM: 123456-SP")
        st.write("Email: medico@medivisao.com")
    elif perfil == "enfermeiro":
        st.image("assets/persona-enfermeira.png", caption="Usuário")
        st.write("Nome completo: Elisangela Cordeiro Botari Freitas")
        st.write("Coren: 78910-SP")
        st.write("Setor: Enfermagem Clínica")
        st.write("Email: enfermeiro@medivisao.com")
    elif perfil == "paciente":
        st.image("assets/persona-paciente.png", caption="Usuário")
        st.write("Nome completo: João Batista Fernandes")
        st.write("Idade: 67")
        st.write("Condições: Hipertensão, Diabetes")
    elif perfil == "administrador":
        st.image("assets/persona-ta.png", caption="Usuário")
        st.write("Nome completo: João Batista Fernandes")
        st.write("Cargo: Técnico Administrativo")
        st.write("Permissões: Gerenciar usuários, criar chamados")

    st.markdown("---")
    if st.button("Editar meus dados"):
        st.info("Funcionalidade de edição em desenvolvimento.")

def pagina_lista_usuarios():
    st.title("Gerenciamento de Usuários")
    st.markdown("🔧 Lista de todos os usuários registrados no sistema.")

    usuarios = st.session_state.get("usuarios", {})
    
    for nome, dados in usuarios.items():
        with st.expander(f"👤 {nome} ({dados['perfil']})"):
            st.write(f"🔐 Senha: `{dados['senha']}`")  # Apenas exemplo — **não exiba senhas em sistemas reais**
            if st.button(f"Editar {nome}", key=f"editar_{nome}"):
                st.info("Funcionalidade de edição em construção.") 

def pagina_analise():
    st.title("Análise de Imagens por Inteligência Artificial")
    st.markdown("Faça upload de imagens para análise médica por IA.")

    imagem = st.file_uploader("Enviar exame (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if imagem:
        st.image(Image.open(imagem), caption="Prévia da imagem", use_column_width=True)
        st.success("Imagem carregada com sucesso. Pronta para análise.")

def pagina_resultado():
    st.title("Resultado da Análise")
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.success("Done!")
    st.warning("⚠️ **80% de chance!** ")
    st.image("assets/analise.png", caption="Imagem com realce automatizado.", use_column_width=True)
    st.markdown("Interpretação")
    st.write("O sistema detectou uma área suspeita. Avaliação adicional recomendada.")
    st.markdown("Áudio descrição")
    st.audio("assets/resultado_analise_audio.mp3")

def pagina_chat():
    st.title("Chat Médico-Paciente")

    if 'chat_log' not in st.session_state:
        st.session_state.chat_log = []

    for msg in st.session_state.chat_log:
        st.markdown(f"**{msg['remetente']}**: {msg['mensagem']}")

    with st.form("chat_form", clear_on_submit=True):
        msg = st.text_input("Mensagem")
        enviar = st.form_submit_button("Enviar")
        if enviar and msg:
            st.session_state.chat_log.append({
                "remetente": st.session_state['perfil'].capitalize(),
                "mensagem": msg
            })

def pagina_chat_enfermeiro():
    st.title("Chat Médico-Enfermeiro")

    if 'chat_log' not in st.session_state:
        st.session_state.chat_log = []

    for msg in st.session_state.chat_log:
        st.markdown(f"**{msg['remetente']}**: {msg['mensagem']}")

    with st.form("chat_form", clear_on_submit=True):
        msg = st.text_input("Mensagem")
        enviar = st.form_submit_button("Enviar")
        if enviar and msg:
            st.session_state.chat_log.append({
                "remetente": st.session_state['perfil'].capitalize(),
                "mensagem": msg
            })

def pagina_prontuario_medico():
    st.title("Prontuário Médico")
    st.markdown("Registro de informações clínicas e observações médicas do paciente.")

    # Inicializa o prontuário apenas uma vez
    if "prontuario_medico" not in st.session_state:
        st.session_state.prontuario_medico = [
            {
                "data": "2024-12-01 14:30",
                "autor": "Dr. João (medico1)",
                "texto": "Paciente relatou dores persistentes no abdômen inferior. Solicitado exame de imagem."
            },
            {
                "data": "2025-03-10 09:00",
                "autor": "Dr. João (medico1)",
                "texto": "Resultado de tomografia aponta alteração compatível com lesão tumoral. Encaminhado para oncologia."
            }
        ]

    # Exibir histórico.
    st.markdown("### 🗂 Histórico do Prontuário")
    for item in reversed(st.session_state.prontuario_medico):
        with st.expander(f"{item['data']} - {item['autor']}"):
            st.markdown(item["texto"])

    # Controle de exibição do formulário
    if "mostrar_form_prontuario" not in st.session_state:
        st.session_state.mostrar_form_prontuario = False

    if st.button("✍️ Nova Anotação"):
        st.session_state.mostrar_form_prontuario = True

    # Formulário para nova anotação
    if st.session_state.mostrar_form_prontuario:
        with st.form("form_prontuario"):
            nova_entrada = st.text_area("Descreva a evolução clínica, queixas, condutas, etc.", height=150)
            salvar = st.form_submit_button("Salvar Anotação")

            if salvar:
                if nova_entrada.strip() == "":
                    st.warning("Por favor, insira uma anotação.")
                else:
                    nova_anotacao = {
                        "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "autor": f"{st.session_state['usuario']} ({st.session_state['perfil']})",
                        "texto": nova_entrada
                    }
                    st.session_state.prontuario_medico.append(nova_anotacao)
                    st.success("Anotação adicionada com sucesso!")
                    st.session_state.mostrar_form_prontuario = False
                    st.rerun()


def pagina_submeter_exames():
    st.title("Submeter Novos Exames")
    st.markdown(" Faça upload de exames para que seu médico possa avaliá-los. 📤")
    imagem = st.file_uploader("Envie um exame", type=["jpg", "png", "jpeg"])
    if imagem:
        st.image(imagem, use_column_width=True)
        st.success("Exame enviado com sucesso!")

def pagina_cadastro_usuario():
    st.title("Cadastro de Usuários")
    st.markdown("Cadastre novos médicos, enfermeiros ou pacientes.")

    with st.form("cad_user_form"):
        novo = st.text_input("Novo usuário")
        senha = st.text_input("Senha", type="password")
        perfil = st.selectbox("Perfil", ["médico", "paciente", "enfermeiro"])
        cadastrar = st.form_submit_button("Cadastrar")

        if cadastrar:
            if novo in st.session_state.usuarios:
                st.error("Usuário já existe.")
            else:
                st.session_state.usuarios[novo] = {"senha": senha, "perfil": perfil}
                st.success("Usuário cadastrado!")

def pagina_chamados_manutencao():
    st.title("Chamados de Manutenção")
    st.markdown("🔧 Registrar problemas técnicos ou solicitações de manutenção.")

    st.text_area("Descreva o problema")
    if st.button("Abrir chamado"):
        st.success("Chamado registrado com sucesso!")


# ========== ROTAS PRINCIPAIS ==========
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# Recuperar página da URL
pagina_atual = st.query_params.get("pagina", "login")

# LÓGICA DE NAVEGAÇÃO
if not st.session_state['autenticado']:
    if pagina_atual == "cadastro":
        cadastro_page()
    else:
        login_page()
else:
    # MENU DINÂMICO POR PERFIL
    with st.sidebar:
        # Logo + Botão logout lado a lado
        col_logo, col_space, col_logout = st.columns([3, 1, 2])
        with col_logo:
            st.image("assets/logo-white.png", use_column_width=True)
        with col_space:
            st.write("     ")    
        with col_logout:
            if st.button("Logout", key="logout", help="Sair"):
                st.session_state['autenticado'] = False
                st.session_state['usuario'] = ""
                st.session_state['perfil'] = ""
                st.query_params["pagina"] = "login"
                st.rerun()

        st.markdown("---")

        perfil = st.session_state['perfil']
        paginas_por_perfil = {
            "médico": {
                "Início": "inicio",
                "Dados Pessoais": "dados_pessoais",
                "Lista de Pacientes": "lista_de_pacientes",
                "Área do Paciente": "area_do_paciente",
            },
            "enfermeiro": {
                "Início": "inicio",
                "Dados Pessoais": "dados_pessoais",
                "Lista de Pacientes": "lista_de_pacientes",
                "Prontuário Médico": "prontuario_medico",
                "Chat Médico-Enfermeiro": "chat_medico_enfermeiro"
            },
            "paciente": {
                "Início": "inicio",
                "Dados Pessoais": "dados_pessoais",
                "Submeter Novos Exames": "submeter_exames",
                "Chat Médico-Paciente": "chat_medico_paciente"
            },
            "administrador": {
                "Início": "inicio",
                "Dados Pessoais": "dados_pessoais",
                "Lista de Usuários": "lista_de_usuários",
                "Cadastro de Usuários": "cadastro_de_usuarios",
                "Chamados de Manutenção": "chamados_de_manutencao"
            }
        }

        menu_labels = list(paginas_por_perfil.get(perfil, {}).keys())
        menu_values = list(paginas_por_perfil.get(perfil, {}).values())

        icon_map = {
            "Início": "house",
            "Lista de Pacientes": "people",
            "Lista de Usuários": "people",
            "Análise de Imagens": "upload",
            "Área do Paciente:": "person-plus",
            "Prontuário Médico": "clipboard",
            "Resultado da Análise": "image",
            "Chat Médico-Paciente": "chat",
            "Chat Médico-Enfermeiro": "chat",
            "Registro de Prontuário": "clipboard-check",
            "Submeter Novos Exames": "cloud-upload",
            "Cadastro de Usuários": "person-plus",
            "Chamados de Manutenção": "tools",
            "Dados Pessoais": "person"
        }

        menu_icons = [icon_map.get(label, "menu") for label in menu_labels]

        menu = option_menu(
            "MENU",
            menu_labels,
            icons=menu_icons,
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"background-color": "white", "padding": "30px"},
                "icon": {"color": "#214c38", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "--hover-color": "#a8d7c0"},
                "nav-link-selected": {"background-color": "#7DA584", "color": "white"},
            }
        )

        st.query_params["pagina"] = paginas_por_perfil[perfil][menu]

        st.markdown("""
            <script>
            const btn = window.parent.document.querySelector('button[kind="primary"][data-testid="baseButton-button"][key="logout"]');
            if (btn) btn.className += " logout-button";
            </script>
        """, unsafe_allow_html=True)    

    # PÁGINAS
    if menu == "Início":
        pagina_inicio()
    elif menu == "Lista de Pacientes":
        pagina_lista_pacientes()
    elif menu == "Lista de Usuários":
        pagina_lista_usuarios()    
    elif menu == "Análise de Imagens":
        pagina_analise()
    elif menu == "Resultado da Análise":
        pagina_resultado()
    elif menu == "Chat Médico-Paciente":
        pagina_chat()
    elif menu == "Chat Médico-Enfermeiro":
        pagina_chat_enfermeiro()    
    elif menu == "Prontuário Médico":
        pagina_prontuario_medico()
    elif menu == "Submeter Novos Exames":
        pagina_submeter_exames()
    elif menu == "Cadastro de Usuários":
        pagina_cadastro_usuario()
    elif menu == "Chamados de Manutenção":
        pagina_chamados_manutencao()
    elif menu == "Dados Pessoais":
        pagina_dados_pessoais()
    elif menu == "Área do Paciente":
        pagina_area_do_paciente()

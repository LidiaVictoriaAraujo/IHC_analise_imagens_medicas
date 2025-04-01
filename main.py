import streamlit as st
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
        border-color: white    
    }
    </style>
""", unsafe_allow_html=True)

# ========== USUÁRIOS ==========
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        "medico1": {"senha": "1234", "perfil": "médico"},
        "paciente1": {"senha": "abcd", "perfil": "paciente"},
        "admin": {"senha": "admin", "perfil": "administrador"},
        "enfermeira1": {"senha": "enf123", "perfil": "enfermeiro"},
        "aaa": {"senha": "aaa", "perfil": "enfermeiro"}
    }

# ========== AUTENTICAÇÃO ==========
def autenticar_usuario(username, senha):
    users = st.session_state.usuarios
    if username in users and users[username]["senha"] == senha:
        return users[username]["perfil"]
    return None

def login_page():
    st.image("assets/logo.png", width=550)
    st.subheader("Sistema Inteligente de Diagnóstico Médico")

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

def pagina_perfil():
    st.title("Perfil do Paciente")
    st.image("assets/persona.png", caption="Paciente")
    st.write("Nome: João Batista Fernandes")
    st.write("Idade: 67 anos")
    st.write("Última consulta: 15/03/2025")
    st.write("Descrição Geral: Aposentado, ex-metalúrgico, hipertenso e diabético ")

    st.markdown("### Histórico Médico com Alertas")
    historico = [
        {"data": "2024-12-01", "evento": "Lesão suspeita detectada", "alerta": True},
        {"data": "2024-06-10", "evento": "Exame de rotina normal", "alerta": False},
        {"data": "2023-11-03", "evento": "Primeira análise automatizada", "alerta": False}
    ]
    for item in historico:
        icon = "⚠️" if item["alerta"] else "✅"
        st.markdown(f"{icon} **{item['data']}** – {item['evento']}")

    # Botões de ação
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Alterar dados cadastrais"):
            st.info("Funcionalidade de edição em construção.")  # Aqui você pode redirecionar ou abrir um form
    with col2:
        if st.button("Carregar novos exames"):
            st.info("Acesse a aba 'Análise de Imagens' para enviar um novo exame.")

def pagina_analise():
    st.title("Análise de Imagens")
    st.markdown("Faça upload de imagens para análise médica.")

    imagem = st.file_uploader("Enviar exame (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if imagem:
        st.image(Image.open(imagem), caption="Prévia da imagem", use_column_width=True)
        st.success("Imagem carregada com sucesso. Pronta para análise.")

def pagina_resultado():
    st.title("Imagem Analisada")
    st.image("assets/analise.png", caption="Imagem com realce automatizado", use_column_width=True)
    st.markdown("### Interpretação")
    st.write("🚨 O sistema detectou uma área suspeita. Avaliação adicional recomendada.")
    st.markdown("### Áudio descrição")
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
    # MENU LATERAL
    with st.sidebar:
        st.logo("assets/logo-white.png", size='large')
        menu = option_menu(
            "MENU",
            ["Início", "Perfil do Paciente", "Análise de Imagens", "Resultado da Análise", "Chat Médico-Paciente"],
            icons=["house", "person", "upload", "image", "chat"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"background-color": "white", "padding": "30px"},
                "icon": {"color": "#214c38", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "--hover-color": "#a8d7c0"},
                "nav-link-selected": {"background-color": "#7DA584", "color": "white"},
            }
        )
        st.query_params["pagina"] = menu.lower().replace(" ", "_")

        st.markdown("---")  # separador visual

        # BOTÃO DE LOGOUT
        if st.button("Logout", key="logout", help="Sair da conta"):
            st.session_state['autenticado'] = False
            st.session_state['usuario'] = ""
            st.session_state['perfil'] = ""
            st.query_params["pagina"] = "login"
            st.rerun()
        
        # Aplicar a classe CSS via JavaScript injection
        st.markdown("""
            <script>
            const btn = window.parent.document.querySelector('button[kind="primary"][data-testid="baseButton-button"][key="logout"]');
            if (btn) btn.className += " logout-button";
            </script>
        """, unsafe_allow_html=True)    

    # PÁGINAS
    if menu == "Início":
        pagina_inicio()
    elif menu == "Perfil do Paciente":
        pagina_perfil()
    elif menu == "Análise de Imagens":
        pagina_analise()
    elif menu == "Resultado da Análise":
        pagina_resultado()
    elif menu == "Chat Médico-Paciente":
        pagina_chat()

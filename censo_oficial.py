import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(
    page_title="I Censo Científico de STP", 
    page_icon="👩🏾‍🔬", 
    layout="wide"
)

# 2. Estilo CSS Personalizado
st.markdown("""
    <style>
    /* Cor de fundo suave */
    .stApp {
        background-color: #fcfcfc;
    }
    /* Estilização do Título */
    .titulo-principal {
        color: #006233; /* Verde da bandeira */
        text-align: center;
        font-weight: bold;
        margin-bottom: 0px;
    }
    /* Estilização da Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6;
        border-right: 2px solid #ed1c24; /* Detalhe em vermelho */
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Configuração da API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Erro: Chave API não encontrada.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 4. BARRA LATERAL (Sidebar)
with st.sidebar:
    st.markdown("## 🇸🇹 I Censo Científico")
    st.info("""
    **Sobre o Censo:**
    Iniciativa para mapear e impulsionar a investigação científica em São Tomé e Príncipe.
    """)
    
    st.divider()
    
    st.markdown("### 📚 Recursos Úteis")
    st.link_button("Manual de Áreas OCDE", "https://www.oecd.org") # Podes mudar o link
    
    st.divider()
    
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

# 5. CABEÇALHO
st.markdown("<h1 class='titulo-principal'>I Censo Científico Nacional de São Tomé e Príncipe</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Portal Oficial de Recolha de Dados e Apoio ao Investigador</p>", unsafe_allow_html=True)
st.write("---")

# 6. LAYOUT EM COLUNAS
col_form, col_bot = st.columns([3, 2], gap="large")

with col_form:
    st.subheader("📝 Formulário do Inquérito")
    # Substitui pelo teu link real do Google Forms
    url_formulario = "https://forms.gle/9d671b4budPBaHS2A"
    st.components.v1.iframe(url_formulario, height=800, scrolling=True)

with col_bot:
    st.subheader("👩🏾‍🔬 Apoio da Dra. Rosa")
    
    # Contentor de chat
    chat_container = st.container(height=600, border=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou a Dra. Rosa. Estou aqui para ajudar a classificar a sua área científica conforme as normas da OCDE. Como posso ajudar?"}
        ]

    with chat_container:
        for message in st.session_state.messages:
            avatar = "👩🏾‍🔬" if message["role"] == "assistant" else None
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # Entrada de texto
    if prompt := st.chat_input("Dúvida na área científica?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container.chat_message("user"):
            st.markdown(prompt)

        with chat_container.chat_message("assistant", avatar="👩🏾‍🔬"):
            try:
                # Instrução de Sistema
                system_prompt = "És a Dra. Rosa, assistente do Censo de STP. Profissional, negra, acolhedora. Ajuda a classificar cursos em: Ciências Naturais, Engenharia, Ciências Médicas, Agrárias, Sociais ou Humanidades."
                
                # Ajustado para o modelo Gemini 3 Flash Preview que tens no AI Studio
                model = genai.GenerativeModel('gemini-3-flash-preview', system_instruction=system_prompt)
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("A Dra. Rosa teve um pequeno problema de ligação. Tente de novo em segundos.")

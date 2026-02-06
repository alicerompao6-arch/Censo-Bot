import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página (Layout Largo para caber os dois)
st.set_page_config(
    page_title="I Censo Científico de STP", 
    page_icon="👩🏾‍🔬", 
    layout="wide" # Isso faz o site usar toda a largura do ecrã
)

# 2. Configuração da API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Erro: Chave API não encontrada.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. Cabeçalho Oficial
st.markdown("<h1 style='text-align: center;'>I Censo Científico Nacional de São Tomé e Príncipe</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'> Preencha o formulário abaixo. Se tiver dúvidas sobre a sua área científica, fale com a Dra. Rosa à direita.</p>", unsafe_allow_html=True)
st.write("---")

# 4. Divisão do Ecrã em Duas Colunas
# Coluna 1: Formulário (60% da largura)
# Coluna 2: Dra. Rosa (40% da largura)
col_form, col_bot = st.columns([3, 2], gap="large")

with col_form:
    st.subheader("📝 Formulário do Inquérito")
    # SUBSTITUA o link abaixo pelo link real do seu formulário (Google Forms, etc.)
    url_formulario = "https://forms.gle/5vJu6dDBiN2o81qP8"
    
    # Este código "incorpora" o formulário dentro do site
    st.components.v1.iframe(url_formulario, height=800, scrolling=True)

with col_bot:
    st.subheader("👩🏾‍🔬 Apoio da Dra. Rosa")
    
    # Inicializar histórico do chat
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou a Dra. Rosa. Se não souber em que área da OCDE enquadrar o seu curso ou investigação no formulário ao lado, diga-me o nome do curso e eu ajudo!"}
        ]

    # Contentor para o chat (com altura fixa para não desformatar a página)
    chat_placeholder = st.container(height=600)

    with chat_placeholder:
        for message in st.session_state.messages:
            avatar = "👩🏾‍🔬" if message["role"] == "assistant" else None
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # Input do Chat
    if prompt := st.chat_input("Dúvida na área científica?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_placeholder.chat_message("user"):
            st.markdown(prompt)

        with chat_placeholder.chat_message("assistant", avatar="👩🏾‍🔬"):
            try:
                # Usando o modelo Gemini 3 Flash conforme configurado antes
                system_prompt = "És a Dra. Rosa, assistente do Censo de STP. Ajuda a classificar cursos nas áreas OCDE."
                model = genai.GenerativeModel('gemini-3-flash-preview', system_instruction=system_prompt)
                response = model.generate_content(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Erro na ligação.")

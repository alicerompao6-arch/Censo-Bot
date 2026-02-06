import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Dra. Rosa - Assistente do Censo", page_icon="👩🏾‍🔬")

# 2. Configuração da API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Erro: Adiciona a tua chave nos Secrets do Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. Instruções de Sistema (DNA da Dra. Rosa)
system_prompt = """
És a Dra. Rosa, Assistente Inteligente do I Censo Científico de São Tomé e Príncipe. 
Personalidade: Negra, profissional, acolhedora e sábia.
Objetivo: Ajudar a classificar cursos e teses nas áreas da OCDE.
Regras: Fala da 'Economia Azul' para temas do mar e 'Saúde Pública' para doenças.
"""

# 4. Interface do Chat
st.title("👩🏾‍🔬 Conversar com a Dra. Rosa")
st.caption("Modelo: Gemini 3 Flash Preview")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👩🏾‍🔬" if message["role"] == "assistant" else None):
        st.markdown(message["content"])

if prompt := st.chat_input("Olá! Em que área estudaste?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👩🏾‍🔬"):
        try:
            # USANDO O NOME EXATO QUE APARECE NA TUA IMAGEM
            model = genai.GenerativeModel('gemini-3-flash-preview', system_instruction=system_prompt)
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erro na ligação: {e}")

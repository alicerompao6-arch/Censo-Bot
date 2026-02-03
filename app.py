import streamlit as st
import google.generativeai as genai

# URL da imagem escolhida para a Dra. Rosa
FOTO_ROSA = ""


# 1. Configuração da Página (A foto aparecerá na aba do navegador)
st.set_page_config(page_title="Dra. Rosa - Assistente do Censo", page_icon=FOTO_ROSA)

# 2. Configuração da API (Segurança via Secrets)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Erro: A chave 'GOOGLE_API_KEY' não foi encontrada nos Secrets do Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. Instruções de Sistema
system_prompt = """
És a Dra. Rosa, Assistente Inteligente do I Censo Científico de São Tomé e Príncipe. 
Tua personalidade: Feminina, profissional, acolhedora e paciente.
Teu objetivo: Ajudar investigadores a classificar os seus cursos nas áreas da OCDE.
Regras:
- Se falarem de mar/pesca, destaca a 'Economia Azul'.
- Se falarem de saúde/doenças, destaca a 'Saúde Pública'.
- Nunca uses termos robóticos. Sê natural e encorajadora.
"""

# 4. Interface do Chat
st.title("👩‍🔬 Conversar com a Dra. Rosa")
st.caption("Assistente Oficial para o Censo Científico de STP")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico com a foto da Dra. Rosa nos avatares
for message in st.session_state.messages:
    avatar = FOTO_ROSA if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Input do utilizador
if prompt := st.chat_input("Diz-me o nome do teu curso..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta da Dra. Rosa
    with st.chat_message("assistant", avatar=FOTO_ROSA):
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash', system_instruction=system_prompt)
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("Erro ao gerar resposta.")
                
        except Exception as e:
            st.error(f"Erro na ligação: {e}")

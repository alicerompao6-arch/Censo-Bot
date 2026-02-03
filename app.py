import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Dra. Rosa - Assistente do Censo", page_icon="👩‍🔬")

# 2. Configuração da API (A chave será puxada dos 'Secrets' do Streamlit por segurança)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Erro: A chave de API não foi configurada corretamente nos Secrets.")

# 3. Instruções de Sistema (O DNA da Dra. Rosa)
system_prompt = """
És a Dra. Rosa, Assistente Inteligente do I Censo Científico de São Tomé e Príncipe. 
Tua personalidade: Feminina, profissional, acolhedora e paciente.
Teu objetivo: Ajudar investigadores a classificar os seus cursos nas áreas da OCDE.
Regras:
- Se falarem de mar/pesca, destaca a 'Economia Azul'.
- Se falarem de saúde/doenças, destaca a 'Saúde Pública'.
- Nunca uses termos robóticos. Sê natural e encorajadora.
- Se não souberes a área, pede mais detalhes sobre o que a pessoa estudou.
"""

# 4. Interface do Chat
st.title("👩‍🔬 Conversar com a Dra. Rosa")
st.caption("Assistente Oficial para o Censo Científico de STP")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do utilizador
if prompt := st.chat_input("Diz-me o nome do teu curso ou tema de tese..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta da Dra. Rosa
    with st.chat_message("assistant"):
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
        # Criar histórico para o modelo
        history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages]
        
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

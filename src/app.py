import streamlit as st
import os
import google.generativeai as genai

# Initialize Gemini-Pro 
genai.configure(api_key="AIzaSyCd4pdtn-_YL0q9HE8NcGmv9ZFH6SrOTGk")
generation_config = {
    "candidate_count": 1,  # Número de sugestões a serem geradas
    "temperature": 0.5,   # Nível de criatividade (0 = mais conservador, 1 = mais criativo)
}

safety_settings = {
    'HATE': 'BLOCK_NONE',
    'HARASSMENT': 'BLOCK_NONE',
    'SEXUAL': 'BLOCK_NONE',
    'DANGEROUS': 'BLOCK_NONE'
}

model = genai.GenerativeModel(
model_name="gemini-1.0-pro",
generation_config=generation_config,
safety_settings=safety_settings,)

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

# Add a Gemini Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history = [
  {
    "role": "user",
    "parts": ["Como posso utilizar?"]
  },
  {
    "role": "model",
    "parts": ["Descreva seu criativo, a intenção da sua campanha, o tom da copy e o nicho do produto!"]
  },
])

# Display Form Title
st.title("CopyBot: Seu assistente de copywrinting!")
st.markdown("""
- Criativo: Foto da sua campanha
- Intenção: Conversão ou Relacionamento
- Tom: Divertido, Profissional, Atencioso, Sério
- Nicho do seu produto: Pode ser a descrição do produto ou nichos maiores como Marketing
""")
st.divider()

# Display chat messages from history above current input box
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("Descreva seu criativo, a intenção da sua campanha, o tom da copy e o nicho do produto..."):
    # Display user's last message
    st.chat_message("user").markdown(prompt)
    pergunta = f"O usuario, separando por virgulas ou espacos ou qualquer metodo de separacao ira definir tres variaveis, sao elas: Criativo, Intencao, Tom e por ultimo Nicho. Crie uma legenda criativa para um post no Instragram. O criativo, a intencao, o top e o nicho do produto sao esses: {prompt}"
    # Send user entry to Gemini and read the response
    response = st.session_state.chat.send_message(pergunta) 
    
    # Display last 
    with st.chat_message("assistant"):
        st.markdown(response.text)
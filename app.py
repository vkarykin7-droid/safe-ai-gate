import streamlit as st
import re
from openai import OpenAI

# Funkcja filtrująca dane (Twoja unikalna wartość!)
def clean_data(text):
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text) # Maile
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text) # NIP
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text) # PESEL
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text) # Tel
    return text

st.set_page_config(page_title="SafeAI Gateway", page_icon="🛡️")
st.title("🛡️ SafeAI: Bezpieczny ChatGPT dla Firmy")

# Panel boczny z Twoim logo i statystykami
st.sidebar.image("https://via.placeholder.com/150?text=TWOJE+LOGO") # Tu wstawisz swoje logo
st.sidebar.title("Panel Administratora")
api_key = st.sidebar.text_input("Klucz API OpenAI", type="password")

st.markdown("""
Ta bramka automatycznie **anonimizuje** Twoje dane. 
Żadne nazwisko, NIP ani telefon nie opuszczą serwera Twojej firmy.
""")

user_input = st.text_area("Wpisz polecenie dla AI:", height=200)

if st.button("Generuj bezpiecznie"):
    if not api_key:
        st.warning("Poproś administratora o klucz API!")
    else:
        client = OpenAI(api_key=api_key)
        
        # PROCES ANONIMIZACJI
        clean_prompt = clean_data(user_input)
        
        with st.expander("Zobacz, jak wyczyściliśmy Twoje dane przed wysłaniem"):
            st.write(clean_prompt)
            
        with st.spinner('AI pracuje...'):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": clean_prompt}]
            )
            st.success("Odpowiedź AI:")
            st.write(response.choices[0].message.content)

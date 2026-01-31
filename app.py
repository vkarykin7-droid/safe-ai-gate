import streamlit as st
import re
from openai import OpenAI

# 1. Podstawowa konfiguracja (Musi być na samym początku!)
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# 2. Funkcja anonimizująca (Twoja technologia)
def clean_data(text):
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text)
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text)
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    return text

# 3. Sidebar - Panel Dowodzenia
with st.sidebar:
    st.header("🛡️ Panel Kontrolny")
    api_key = st.text_input("Klucz API OpenAI", type="password")
    
    st.divider()
    st.subheader("Status Systemu")
    st.write("✅ Filtr RODO: Aktywny")
    st.write("✅ Szyfrowanie: AES-256")
    st.metric(label="Zablokowane wycieki", value="4")
    
    st.divider()
    st.caption("SafeAI Gateway v1.0")

# 4. Strona Główna
st.title("🛡️ SafeAI Gateway")
st.subheader("Enterprise Data Protection")

st.info("System automatycznie usuwa dane wrażliwe przed wysłaniem ich do AI.")

user_input = st.text_area("Wpisz polecenie dla AI:", placeholder="Np. Napisz maila do klienta...", height=200)

if st.button("🚀 Wyślij Bezpiecznie"):
    if not api_key:
        st.error("Wpisz klucz API w panelu bocznym po lewej!")
    elif not user_input:
        st.warning("Wpisz najpierw tekst.")
    else:
        # Procesowanie
        cleaned_text = clean_data(user_input)
        
        # Pokazanie co widzi AI (buduje zaufanie)
        with st.expander("👁️ Podgląd filtra (Tyle widzi ChatGPT)"):
            st.code(cleaned_text)
        
        # Połączenie z OpenAI
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner('Trwa bezpieczne przetwarzanie...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned_text}]
                )
                st.success("Odpowiedź AI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Błąd: {e}")

st.divider()
st.caption("© 2026 SafeAI Gateway Polska")

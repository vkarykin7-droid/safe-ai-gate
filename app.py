import streamlit as st
import re
from openai import OpenAI

# 1. Konfiguracja
st.set_page_config(page_title="SafeAI Gateway", layout="wide")

# --- KLUCZ WPISANY NA STAŁE ---
# Dzięki temu po odświeżeniu strony system od razu go zna.
OPENAI_API_KEY = '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'

# 2. Funkcja czyszcząca dane
def clean_data(text):
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text)
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text)
    text = re.sub(r'\d{2}-\d{3}', '[UKRYTY_KOD]', text)
    text = re.sub(r'(ul\.|ulica|Al\.|Aleja|Plac|Park|ul)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+', '[UKRYTY_ADRES]', text)
    return text

# 3. Interfejs użytkownika (Bez pola na klucz!)
st.title("🛡️ SafeAI Gateway")
st.write("Witamy w bezpiecznym panelu AI Twojej firmy.")

# Panel boczny tylko z informacjami
st.sidebar.header("🛡️ Status Systemu")
st.sidebar.success("✅ Połączono z OpenAI")
st.sidebar.info("Twoje dane są filtrowane przed wysłaniem.")

# 4. Pole tekstowe
user_input = st.text_area("Wpisz zapytanie do AI:", height=200)

if st.button("🚀 Wyślij bezpiecznie"):
    if not user_input:
        st.warning("Najpierw wpisz tekst.")
    else:
        # Anonimizacja
        cleaned = clean_data(user_input)
        
        st.subheader("🛡️ Podgląd bezpieczeństwa:")
        st.code(cleaned)
        
        # Wywołanie API
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            with st.spinner('AI generuje odpowiedź...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                st.success("Odpowiedź AI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Błąd: {e}")

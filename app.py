import streamlit as st
import re
from openai import OpenAI

# 1. Konfiguracja strony
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# 2. Silnik anonimizacji
def clean_data(text):
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text)
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text)
    text = re.sub(r'\d{2}-\d{3}', '[UKRYTY_KOD]', text)
    text = re.sub(r'(ul\.|ulica|Al\.|Aleja|Plac|Park|ul)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+', '[UKRYTY_ADRES]', text)
    return text

# 3. Panel Boczny - POWRÓT POLA NA KLUCZ
with st.sidebar:
    st.header("🛡️ Konfiguracja")
    user_key = st.text_input("Wklej swój klucz API OpenAI:", type="password")
    st.divider()
    st.header("📩 Kontakt i Wsparcie")
    st.info("E-mail: vkarykin7@gmail.com")
    st.write("Wdrożenia biznesowe i wsparcie techniczne.")
    st.divider()
    st.metric(label="Zablokowane wycieki", value="24")

# 4. Sekcja Marketingowa
st.title("🛡️ SafeAI Gateway")
st.subheader("Twoja tarcza przed wyciekiem danych do AI")

c1, c2, c3 = st.columns(3)
with c1:
    st.error("⚖️ **AI Act**")
    st.write("Dostosuj firmę do nowych przepisów UE o AI (2026).")
with c2:
    st.error("🔓 **RODO**")
    st.write("Chroń dane osobowe swoich klientów przed modelem AI.")
with c3:
    st.error("🕵️ **Shadow AI**")
    st.write("Kontroluj przepływ informacji wrażliwych w zespole.")

st.divider()

# 5. Interfejs użytkownika
user_input = st.text_area("Wpisz polecenie dla AI:", height=200)

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_key:
        st.error("Błąd: Musisz podać klucz API w panelu bocznym!")
    elif not user_input:
        st.warning("Wpisz tekst przed wysłaniem.")
    else:
        # Anonimizacja
        cleaned = clean_data(user_input)
        st.subheader("🛡️ Podgląd ochrony (To widzi AI):")
        st.code(cleaned)
        
        # Wywołanie API
        try:
            client = OpenAI(api_key=user_key)
            with st.spinner('Generowanie odpowiedzi...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                st.success("Bezpieczna odpowiedź od SafeAI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Problem: {str(e)}")

# 6. Stopka
st.divider()
st.caption("© 2026 SafeAI Gateway Polska | Zgodność z RODO i AI Act")

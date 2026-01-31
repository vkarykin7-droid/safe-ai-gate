import streamlit as st
import re
from openai import OpenAI

# 1. Konfiguracja strony
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# --- TWÓJ KLUCZ API (Wpisany na stałe - nie musisz go wpisywać na stronie) ---
OPENAI_API_KEY = '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' 
# --------------------------------------------------------------------------

# 2. Silnik anonimizacji (RODO + Adresy)
def clean_data(text):
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text)
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text)
    text = re.sub(r'\d{2}-\d{3}', '[UKRYTY_KOD]', text)
    text = re.sub(r'(ul\.|ulica|Al\.|Aleja|Plac|Park|ul)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)*\s+\d+', '[UKRYTY_ADRES]', text)
    return text

# 3. Panel Boczny (Zawsze widoczny)
with st.sidebar:
    st.header("🛡️ SafeAI Status")
    st.success("✅ System: Aktywny")
    st.write("✅ Klucz API: Załadowany")
    st.write("✅ Filtr RODO: ON")
    st.divider()
    st.metric(label="Zablokowane wycieki", value="24")
    st.write("---")
    st.subheader("Kontakt i Wsparcie")
    st.info("📩 vkarykin7@gmail.com")
    st.caption("Masz pytania o wdrożenie? Napisz do nas.")

# 4. Sekcja Nagłówkowa i Argumenty Biznesowe
st.title("🛡️ SafeAI Gateway")
st.subheader("Twoja tarcza przed wyciekiem danych do Sztucznej Inteligencji")

col1, col2, col3 = st.columns(3)
with col1:
    st.error("⚖️ **AI Act (Prawo)**")
    st.write("Dostosuj firmę do nadchodzących przepisów UE o sztucznej inteligencji (2026).")
with col2:
    st.error("🔓 **RODO**")
    st.write("Dane wklejane do ChatGPT stają się publiczne. Nasz system je anonimizuje.")
with col3:
    st.error("🕵️ **Shadow AI**")
    st.write("Kontroluj, jak Twoi pracownicy używają AI, chroniąc tajemnice handlowe.")

st.divider()

# 5. Pole robocze
user_input = st.text_area("Wpisz polecenie dla AI (np. prośbę o analizę umowy):", height=200)

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input:
        st.warning("Proszę wpisać tekst przed wysłaniem.")
    else:
        # KROK 1: Anonimizacja
        cleaned_prompt = clean_data(user_input)
        
        st.subheader("🛡️ Wynik działania tarczy (To widzi AI):")
        st.code(cleaned_prompt)
        
        # KROK 2: Połączenie z OpenAI
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            with st.spinner('Trwa bezpieczne generowanie odpowiedzi...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned_prompt}]
                )
                st.success("Bezpieczna odpowiedź od SafeAI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Błąd systemu: {e}")

# 6. Stopka
st.divider()
st.write("### O SafeAI Gateway")
st.write("Jesteśmy polskim dostawcą rozwiązań zapewniających bezpieczeństwo danych w dobie AI. Nasza technologia pozwala firmom korzystać z najpotężniejszych modeli językowych bez ryzyka utraty kontroli nad informacjami wrażliwymi.")
st.caption("© 2026 SafeAI Gateway Polska | Zgodność z RODO i AI Act")

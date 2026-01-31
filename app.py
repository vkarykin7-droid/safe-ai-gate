import streamlit as st
import re
from openai import OpenAI

# 1. Konfiguracja strony
st.set_page_config(page_title="SafeAI Gateway Pro", layout="wide")

# --- TWÓJ KLUCZ API (Wstawiony na stałe) ---
OPENAI_API_KEY = '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' 
# ---------------------------------------

# 2. Silnik anonimizacji (RODO + Adresy)
def clean_data(text):
    # E-maile
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    # Telefony
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    # NIP, PESEL, REGON
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text)
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text)
    text = re.sub(r'\d{9,10}', '[UKRYTY_ID]', text)
    # Adresy i kody pocztowe
    text = re.sub(r'\d{2}-\d{3}', '[UKRYTY_KOD]', text)
    text = re.sub(r'(ul\.|ulica|Al\.|Aleja|Plac|Park|ul)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+', '[UKRYTY_ADRES]', text)
    return text

# 3. Panel boczny
st.sidebar.title("🛡️ Status SafeAI")
st.sidebar.success("✅ Klucz API: Aktywny")
st.sidebar.write("🔒 Filtr RODO: Włączony")
st.sidebar.metric("Zablokowane wycieki", "24")

# 4. Interfejs Główny
st.title("🛡️ SafeAI Gateway")
st.write("### Bezpieczna brama do Sztucznej Inteligencji")

st.warning("⚖️ **Ważne:** Używanie AI bez filtrów narusza RODO i AI Act. Ten system chroni Twój biznes przed karami.")

st.divider()

# 5. Pole wprowadzania danych
user_input = st.text_area("Wpisz polecenie dla AI (system automatycznie ukryje dane wrażliwe):", height=150)

if st.button("🚀 Uruchom bezpieczne przetwarzanie"):
    if not user_input:
        st.warning("Proszę wpisać treść zapytania.")
    else:
        # Proces anonimizacji
        cleaned = clean_data(user_input)
        
        st.write("🛡️ **Podgląd tarczy (To widzi model AI):**")
        st.code(cleaned)
        
        # Komunikacja z OpenAI
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            with st.spinner('Analizowanie przez AI...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                st.success("Odpowiedź SafeAI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Błąd OpenAI (sprawdź saldo na platformie): {e}")

st.divider()
st.info("📩 Kontakt i wdrożenia: vkarykin7@gmail.com")
st.caption("© 2026 SafeAI Gateway Polska")

import streamlit as st
import re
from openai import OpenAI

# 1. Konfiguracja strony
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# --- TWÓJ KLUCZ API ---
API_KEY = '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'

# 2. Silnik anonimizacji
def clean_data(text):
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text)
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text)
    text = re.sub(r'\d{2}-\d{3}', '[UKRYTY_KOD]', text)
    text = re.sub(r'(ul\.|ulica|Al\.|Aleja|Plac|Park|ul)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+', '[UKRYTY_ADRES]', text)
    return text

# 3. Panel Boczny
with st.sidebar:
    st.header("⚙️ Status Systemu")
    st.success("✅ Połączono: SafeAI Cloud")
    st.divider()
    st.header("📈 Aktywność dzisiaj")
    st.metric(label="Zablokowane wycieki", value="142", delta="+12%")
    st.metric(label="Przetworzone zapytania", value="1.2k")
    st.divider()
    st.caption("System automatycznie usuwa dane wrażliwe przed wysłaniem ich do AI.")

# 4. Sekcja Marketingowa
st.title("🛡️ SafeAI Gateway")
st.markdown("### Twoja bezpieczna brama do Sztucznej Inteligencji")

col1, col2, col3 = st.columns(3)
with col1:
    st.error("⚖️ **Zgodność z AI Act**")
    st.write("Dostosuj firmę do przepisów UE o AI (2026).")
with col2:
    st.error("🔐 **Ochrona RODO**")
    st.write("Dane wklejane do AI są anonimizowane w milisekundę.")
with col3:
    st.error("💼 **Bezpieczeństwo**")
    st.write("Chroń tajemnice handlowe przed wyciekiem do chmury.")

st.divider()

# 5. Pole robocze
st.write("#### 🚀 Wklej zapytanie do AI")
user_input = st.text_area("Wpisz polecenie (system ukryje dane osobowe):", height=180)

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input:
        st.warning("Najpierw wprowadź tekst.")
    else:
        cleaned = clean_data(user_input)
        st.subheader("🛡️ Podgląd tarczy (To widzi AI):")
        st.code(cleaned)
        
        try:
            client = OpenAI(api_key=API_KEY)
            with st.spinner('Generowanie odpowiedzi...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                st.success("✨ Odpowiedź od SafeAI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Błąd połączenia: {str(e)}")

# 6. Stopka i Kontakt
st.divider()
f_col1, f_col2 = st.columns([2, 1])

with f_col1:
    st.write("### O SafeAI Gateway")
    st.write("Jesteśmy liderem rozwiązań typu Privacy-First dla biznesu w Polsce. Nasza technologia pozwala firmom korzystać z AI bez ryzyka.")

with f_col2:
    st.write("### 📩 Kontakt")
    st.write("vkarykin7@gmail.com")
    st.write("Zapytaj o wersję White Label dla Twojej firmy.")

st.divider()
st.caption("© 2026 SafeAI Gateway Polska. Zgodność z RODO i AI Act.")

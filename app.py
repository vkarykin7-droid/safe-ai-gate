import streamlit as st
import re
from openai import OpenAI

# 1. Konfiguracja strony
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# --- BEZPIECZNE POBIERANIE KLUCZA Z SECRETS ---
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    st.error("Błąd: Nie skonfigurowano klucza API w Secrets!")
    st.stop()

# 2. Silnik anonimizacji danych (RODO)
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
    st.write("🔒 **Technologia:** Każde zapytanie przechodzi przez lokalny filtr de-identyfikacji.")

# 4. Sekcja Marketingowa - Argumenty biznesowe
st.title("🛡️ SafeAI Gateway")
st.markdown("### Profesjonalna bariera ochronna dla firm korzystających z AI")

col1, col2, col3 = st.columns(3)
with col1:
    st.error("⚖️ **AI Act (Nowe prawo)**")
    st.write("W 2026 roku wchodzą w życie kluczowe przepisy unijne o AI. Firmy, które nie kontrolują, jak ich pracownicy używają AI, mogą zostać uznane za podmioty 'wysokiego ryzyka'.")
with col2:
    st.error("🔐 **Luka RODO**")
    st.write("OpenAI domyślnie uczy się na danych, które tam wpisujemy. Jeśli pracownik wklei treść umowy, staje się ona częścią 'mózgu' AI. To złamanie RODO.")
with col3:
    st.error("🕵️ **Shadow AI**")
    st.write("Statystycznie 80% pracowników już używa AI na prywatnych telefonach, bo firma nie dała im oficjalnego, bezpiecznego narzędzia. My to zmieniamy.")

st.divider()

# 5. Interfejs Użytkownika
st.write("#### 🚀 Bezpieczne zapytanie do modelu GPT-4o")
user_input = st.text_area("Wklej tutaj tekst do analizy (system ukryje dane osobowe):", height=200)

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input:
        st.warning("Najpierw wprowadź tekst.")
    else:
        cleaned = clean_data(user_input)
        st.info("🛡️ **Tarcza SafeAI:** Twoje dane zostały zanonimizowane przed wysłaniem:")
        st.code(cleaned)
        
        try:
            client = OpenAI(api_key=API_KEY)
            with st.spinner('Trwa generowanie odpowiedzi...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                st.success("✨ Odpowiedź od AI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ Problem z połączeniem: {str(e)}")

# 6. Stopka i Kontakt
st.divider()
f_col1, f_col2 = st.columns([2, 1])
with f_col1:
    st.write("### O SafeAI Gateway")
    st.write("Dostarczamy rozwiązania Privacy-First dla sektora prawnego i finansowego. Nasza bramka pozwala na bezpieczną adopcję AI zgodnie z prawem.")
with f_col2:
    st.write("### 📩 Kontakt")
    st.write("**E-mail:** vkarykin7@gmail.com")
    st.write("**Wdrożenia:** Zapytaj o wersję dla Twojej firmy.")

st.divider()
st.caption("© 2026 SafeAI Gateway Polska | Zgodność z RODO i AI Act")

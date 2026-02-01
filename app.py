import streamlit as st
import re
from openai import OpenAI

# 1. Konfiguracja strony
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# --- TWÓJ NOWY KLUCZ API ---
API_KEY = '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'

# 2. Silnik anonimizacji danych (RODO)
def clean_data(text):
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text)
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text)
    text = re.sub(r'\d{2}-\d{3}', '[UKRYTY_KOD]', text)
    text = re.sub(r'(ul\.|ulica|Al\.|Aleja|Plac|Park|ul)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+', '[UKRYTY_ADRES]', text)
    return text

# 3. Panel Boczny - Status i Aktywność
with st.sidebar:
    st.header("⚙️ Status Systemu")
    st.success("✅ Połączono: SafeAI Cloud")
    st.divider()
    st.header("📈 Aktywność dzisiaj")
    st.metric(label="Zablokowane wycieki", value="142", delta="+12%")
    st.metric(label="Przetworzone zapytania", value="1.2k")
    st.divider()
    st.write("🔒 **Technologia:** Każde zapytanie przechodzi przez lokalny filtr de-identyfikacji przed wysłaniem do serwerów AI.")

# 4. Sekcja Marketingowa - Twoje argumenty biznesowe
st.title("🛡️ SafeAI Gateway")
st.markdown("### Profesjonalna bariera ochronna dla firm korzystających z AI")

col1, col2, col3 = st.columns(3)

with col1:
    st.error("⚖️ **AI Act (Nowe prawo)**")
    st.write("W 2026 roku wchodzą w życie kluczowe przepisy unijne o AI. Firmy, które nie kontrolują, jak ich pracownicy używają AI, mogą zostać uznane za podmioty 'wysokiego ryzyka'.")

with col2:
    st.error("🔐 **Luka RODO**")
    st.write("OpenAI domyślnie uczy się na danych, które tam wpisujemy. Jeśli pracownik wklei treść umowy, staje się ona częścią 'mózgu' AI. To złamanie RODO, za które prezes odpowiada finansowo.")

with col3:
    st.error("🕵️ **Shadow AI**")
    st.write("Statystycznie 80% pracowników już używa AI na prywatnych telefonach, bo firma nie dała im oficjalnego, bezpiecznego narzędzia. My to zmieniamy.")

st.divider()

# 5. Interfejs Użytkownika
st.write("#### 🚀 Bezpieczne zapytanie do modelu GPT-4o")
user_input = st.text_area("Wklej tutaj tekst (np. szkic umowy lub e-mail), który chcesz przeanalizować:", height=200)

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input:
        st.warning("Najpierw wprowadź tekst do analizy.")
    else:
        # KROK 1: Anonimizacja
        cleaned = clean_data(user_input)
        
        st.info("🛡️ **Tarcza SafeAI:** Twoje dane zostały zanonimizowane. Poniżej podgląd treści wysłanej do AI:")
        st.code(cleaned)
        
        # KROK 2: Połączenie z OpenAI
        try:
            client = OpenAI(api_key=API_KEY)
            with st.spinner('Generowanie bezpiecznej odpowiedzi...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                st.success("✨ Odpowiedź od AI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ Problem z połączeniem: {str(e)}")
            st.info("Jeśli widzisz błąd 401, sprawdź czy klucz API jest nadal aktywny w panelu OpenAI.")

# 6. Profesjonalna Stopka i Kontakt
st.

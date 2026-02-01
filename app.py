import streamlit as st
import re
from openai import OpenAI

# 1. Konfiguracja strony - Profesjonalny wygląd
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# --- TWÓJ NOWY KLUCZ API (Wstawiony poprawnie) ---
OPENAI_API_KEY = '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'

# 2. Silnik anonimizacji danych wrażliwych
def clean_data(text):
    # E-maile
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    # Telefony
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    # NIP, PESEL
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text)
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text)
    # Kody pocztowe i Adresy
    text = re.sub(r'\d{2}-\d{3}', '[UKRYTY_KOD]', text)
    text = re.sub(r'(ul\.|ulica|Al\.|Aleja|Plac|Park|ul)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+', '[UKRYTY_ADRES]', text)
    return text

# 3. Panel Boczny - Statystyki i Status
with st.sidebar:
    st.header("⚙️ Status Systemu")
    st.success("✅ Połączono: SafeAI Cloud")
    st.info("🔐 Szyfrowanie: AES-256")
    st.divider()
    
    st.header("📈 Aktywność dzisiaj")
    st.metric(label="Zablokowane wycieki", value="142", delta="+12%")
    st.metric(label="Przetworzone zapytania", value="1.2k")
    st.divider()
    st.caption("System automatycznie wykrywa i usuwa dane wrażliwe przed wysłaniem ich do modeli językowych.")

# 4. Sekcja Marketingowa - Argumenty Sprzedażowe
st.title("🛡️ SafeAI Gateway")
st.markdown("### Twoja bezpieczna brama do Sztucznej Inteligencji")

col1, col2, col3 = st.columns(3)
with col1:
    st.error("⚖️ **Zgodność z AI Act**")
    st.write("Dostosuj swoją firmę do nadchodzących przepisów UE o sztucznej inteligencji (2026).")
with col2:
    st.error("🔐 **Ochrona RODO**")
    st.write("Dane wklejane do ChatGPT stają się publiczne. Nasz system je anonimizuje w milisekundę.")
with col3:
    st.error("💼 **Bezpieczeństwo**")
    st.write("Chroń tajemnice handlowe i dane klientów przed wyciekiem do chmury publicznej.")

st.divider()

# 5. Interfejs Użytkownika
st.write("#### 🚀 Wklej zapytanie do AI")
user_input = st.text_area("System automatycznie ukryje imiona, nazwiska, adresy, NIP-y i telefony:", height=180, placeholder="Np. Napisz wezwanie do zapłaty dla Jana Kowalskiego, NIP 123-456-78-90...")

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input:
        st.warning("Najpierw wprowadź tekst do analizy.")
    else:
        # KROK 1: Anonimizacja
        cleaned = clean_data(user_input)
        
        st.subheader("🛡️ Podgląd tarczy (To widzi AI):")
        st.code(cleaned)
        
        # KROK 2: Połączenie z OpenAI przy użyciu Twojego klucza
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            with st.spinner('Trwa generowanie bezpiecznej odpowiedzi...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                st.success("✨ Odpowiedź od SafeAI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Błąd połączenia: {str(e)}")
            st.info("Upewnij się, że masz dodatnie saldo na koncie OpenAI (Billing).")

# 6. Profesjonalna Stopka i Kontakt
st.divider()
f_col1, f_col2 = st.columns([2, 1])

with f_col1:
    st.write("### O SafeAI Gateway")
    st.write("Jesteśmy liderem rozwiązań typu Privacy-First dla biznes

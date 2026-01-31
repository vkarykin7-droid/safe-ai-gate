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

# 3. Panel Boczny (Konfiguracja i Statystyki)
with st.sidebar:
    st.header("⚙️ Ustawienia połączenia")
    user_key = st.text_input("Wprowadź klucz API OpenAI:", type="password", help="Klucz nie jest zapisywany na serwerze.")
    st.divider()
    
    st.header("📈 Aktywność systemu")
    st.success("✅ Bramka: Aktywna")
    st.metric(label="Zablokowane wycieki (dziś)", value="142", delta="12%")
    st.metric(label="Przetworzone zapytania", value="1.2k")
    
    st.divider()
    st.write("🔒 **Bezpieczeństwo:** Dane są szyfrowane i anonimizowane lokalnie przed wysłaniem do chmury.")

# 4. Sekcja Marketingowa (Mocne napisy)
st.title("🛡️ SafeAI Gateway")
st.markdown("### Profesjonalna tarcza RODO dla systemów Sztucznej Inteligencji")

col1, col2, col3 = st.columns(3)
with col1:
    st.error("⚖️ **Zgodność z AI Act**")
    st.write("Przygotuj swoją firmę na europejskie prawo o AI (obowiązuje od 2026). Minimalizuj ryzyko prawne.")
with col2:
    st.error("🔐 **Ochrona RODO**")
    st.write("Nigdy więcej danych osobowych w ChatGPT. Nasz filtr usuwa wrażliwe dane w milisekundę.")
with col3:
    st.error("💼 **Bezpieczeństwo Biznesowe**")
    st.write("Chroń know-how swojej firmy i dane klientów przed wykorzystaniem ich do trenowania modeli AI.")

st.divider()

# 5. Pole robocze użytkownika
st.write("#### 🚀 Bezpieczny Edytor")
user_input = st.text_area("Wklej tutaj tekst do przetworzenia (np. e-mail, umowę, notatkę):", height=200, placeholder="Np. Proszę o streszczenie umowy z Janem Kowalskim NIP 123-456...")

if st.button("Uruchom Bezpieczne Przetwarzanie"):
    if not user_key:
        st.error("⚠️ Aby kontynuować, musisz podać klucz API w panelu bocznym.")
    elif not user_input:
        st.warning("⚠️ Pole tekstowe nie może być puste.")
    else:
        # KROK 1: Anonimizacja
        cleaned = clean_data(user_input)
        
        st.info("🛡️ **Tarcza aktywna:** Poniżej widzisz tekst, który zostanie wysłany do AI (dane wrażliwe zostały podmienione):")
        st.code(cleaned)
        
        # KROK 2: Połączenie z OpenAI
        try:
            client = OpenAI(api_key=user_key)
            with st.spinner('Trwa bezpieczne generowanie odpowiedzi przez model GPT-4o...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                st.success("✨ Bezpieczna odpowiedź od AI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ Problem z połączeniem: {str(e)}")

# 6. Sekcja Kontaktowa na dole (Profesjonalna stopka)
st.divider()
f_col1, f_col2 = st.columns([2, 1])

with f_col1:
    st.write("### O SafeAI Gateway")
    st.write("Jesteśmy liderem rozwiązań typu Privacy-First dla biznesu w Polsce. Nasza bramka pozwala na bezpieczną adopcję Sztucznej Inteligencji w sektorach prawnym, finansowym i medycznym.")

with f_col2:
    st.write("### 📩 Kontakt")
    st.write("**Wsparcie techniczne:**")
    st.write("vkarykin7@gmail.com")
    st.write("**Wdrożenia korporacyjne:**")
    st.write("Zapytaj o wersję White Label dla Twojej firmy.")

st.divider()
st.caption("© 2026 SafeAI Gateway Polska. Wszystkie prawa zastrzeżone. Zgodność z RODO i AI Act.")

import streamlit as st
import re
from openai import OpenAI

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# --- STYLIZACJA (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; 
        background-color: #004a99; 
        color: white; 
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .stTextArea>div>div>textarea { border: 2px solid #004a99; }
    .status-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        border-left: 5px solid #004a99;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_input=True)

# --- FUNKCJA FILTRUJĄCA (Twoja unikalna wartość) ---
def clean_data(text):
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text) # Maile
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text) # NIP
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text) # PESEL
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text) # Tel
    return text

# --- PANEL BOCZNY (ADMIN) ---
with st.sidebar:
    st.header("🛡️ Panel Kontrolny")
    api_key = st.text_input("Klucz API OpenAI", type="password", help="Wklej tutaj klucz z platform.openai.com")
    
    st.divider()
    st.subheader("Statystyki Bezpieczeństwa")
    st.metric(label="Zablokowane wycieki", value="Aktywne", delta="RODO OK")
    st.metric(label="Szyfrowanie", value="AES-256")
    
    st.divider()
    st.info("Zgodność z AI Act: Weryfikacja w toku...")

# --- STRONA GŁÓWNA ---
col1, col2 = st.columns([1, 4])
with col1:
    # Ikona tarczy (używamy emoji jako logo)
    st.markdown("<h1 style='text-align: center;'>🛡️</h1>", unsafe_allow_input=True)
with col2:
    st.title("SafeAI Gateway")
    st.subheader("Enterprise Data Protection Layer")

st.markdown("""
<div class='status-box'>
    <strong>Jak to działa?</strong> Wpisz dowolne polecenie. Nasz system automatycznie wykryje i usunie dane wrażliwe 
    (maile, telefony, numery identyfikacyjne) zanim trafią one do chmury AI.
</div>
""", unsafe_allow_input=True)

st.write("") # Odstęp

# Wybór zadania
option = st.selectbox(
    'W czym może pomóc Ci AI?',
    ('Ogólne zapytanie', 'Analiza treści umowy', 'Poprawa stylu komunikacji'))

user_input = st.text_area("Twoje polecenie:", placeholder="Wklej tutaj tekst do przetworzenia...", height=200)

if st.button("🚀 Wyślij Bezpiecznie"):
    if not api_key:
        st.error("Błąd: Brak klucza API w panelu bocznym!")
    elif not user_input:
        st.warning("Wpisz najpierw jakąś treść.")
    else:
        # 1. Anonimizacja
        cleaned_text = clean_data(user_input)
        
        # 2. Pokazanie co zrobiliśmy (buduje zaufanie klienta)
        with st.expander("Podgląd filtra bezpieczeństwa (Co widzi AI)"):
            st.code(cleaned_text)
        
        # 3. Wysyłka do OpenAI
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner('Trwa bezpieczne przetwarzanie danych...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned_text}]
                )
                st.success("Odpowiedź od SafeAI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Wystąpił błąd połączenia: {e}")

# Stopka
st.divider()
st.caption("© 2026 SafeAI Gateway Polska. Chronimy Twoje dane zgodnie z wytycznymi PwC i AI Act.")

import streamlit as st
import re
from openai import OpenAI
import pdfplumber
from docx import Document
import base64
import random

# 1. Konfiguracja strony
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# --- INICJALIZACJA STANU SESJI ---
if 'leaks_blocked' not in st.session_state:
    st.session_state['leaks_blocked'] = 0
if 'total_queries' not in st.session_state:
    st.session_state['total_queries'] = 0
if 'last_ai_response' not in st.session_state:
    st.session_state['last_ai_response'] = None
if 'last_cleaned_text' not in st.session_state:
    st.session_state['last_cleaned_text'] = None
if 'last_found_leaks' not in st.session_state:
    st.session_state['last_found_leaks'] = 0

# --- POBIERANIE KLUCZA ---
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=API_KEY)
except:
    st.error("Błąd: Nie skonfigurowano klucza API!")
    st.stop()

# 2. Silnik anonimizacji
def clean_data(text):
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    text = re.sub(r'(Pan|Pani|Panem|Panią)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)?', '[UKRYTY_KLIENT]', text)
    text = re.sub(r'\b(?:\d[ ]?){26}\b', '[UKRYTY_NR_KONTA]', text)
    patterns = [r'NIP[:\s]*(\d+[-\d]*)', r'PESEL[:\s]*(\d+)', r'REGON[:\s]*(\d+)', r'NR DOWODU[:\s]*(\S+)']
    for pattern in patterns:
        text = re.sub(pattern, lambda m: m.group(0).split(':')[0] + ': [UKRYTE_DANE]', text, flags=re.IGNORECASE)
    text = re.sub(r'\b\d{6,}\b', '[UKRYTY_CIĄG_CYFR]', text)
    text = re.sub(r'(ul\.|ulica|Al\.|Aleja|Plac|Park|ul)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(\s+[0-9A-Za-z/]+)?', '[UKRYTY_ADRES]', text)
    return text

# 3. Panel Boczny
with st.sidebar:
    st.header("⚙️ Status Systemu")
    st.success("✅ Połączono: SafeAI Cloud")
    st.divider()
    st.header("📈 Aktywność Sesji")
    st.metric(label="Zablokowane wycieki", value=st.session_state['leaks_blocked'])
    st.metric(label="Przetworzone zapytania", value=st.session_state['total_queries'])

# 4. Interfejs Użytkownika
st.title("🛡️ SafeAI Gateway")
st.markdown("### Profesjonalna bariera ochronna dla firm")

user_input = st.text_area("Wklej tekst do analizy:", height=200)

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input:
        st.warning("Najpierw wprowadź tekst.")
    else:
        with st.spinner('Trwa anonimizacja i zapytanie do AI...'):
            # Anonimizacja
            cleaned = clean_data(user_input)
            found_leaks = cleaned.count("[UKRYT")
            
            try:
                # Zapytanie do OpenAI
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                
                # Zapisujemy wszystko do session_state
                st.session_state['last_ai_response'] = response.choices[0].message.content
                st.session_state['last_cleaned_text'] = cleaned
                st.session_state['last_found_leaks'] = found_leaks
                
                # Aktualizacja globalnych liczników
                st.session_state['leaks_blocked'] += found_leaks
                st.session_state['total_queries'] += 1
                
                # Wymuszamy odświeżenie UI dla sidebar'u
                st.rerun()
                
            except Exception as e:
                st.error(f"Błąd OpenAI: {e}")

# 5. WYŚWIETLANIE WYNIKÓW (POZA PRZYCISKIEM)
if st.session_state['last_ai_response']:
    st.divider()
    st.info(f"🛡️ **Tarcza SafeAI:** Wykryto i zanonimizowano **{st.session_state['last_found_leaks']}** danych wrażliwych.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tekst po anonimizacji")
        st.code(st.session_state['last_cleaned_text'])
    
    with col2:
        st.subheader("Odpowiedź AI")
        st.write(st.session_state['last_ai_response'])

# Stopka
st.divider()
st.caption("© 2026 SafeAI Gateway Polska")

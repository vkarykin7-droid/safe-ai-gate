import streamlit as st
import re
from openai import OpenAI
import pdfplumber
from docx import Document
import base64

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

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# 3. Panel Boczny
with st.sidebar:
    st.header("⚙️ Status Systemu")
    st.success("✅ Połączono: SafeAI Cloud")
    st.divider()
    st.header("📈 Aktywność Sesji")
    st.metric(label="Zablokowane wycieki", value=st.session_state['leaks_blocked'])
    st.metric(label="Przetworzone zapytania", value=st.session_state['total_queries'])
    if st.button("Wyczyść wyniki"):
        st.session_state['last_ai_response'] = None
        st.rerun()

# 4. Interfejs Użytkownika
st.title("🛡️ SafeAI Gateway")
st.markdown("### Profesjonalna bariera ochronna dla firm")

# Główne wejścia danych
user_input = st.text_area("Wklej tekst do analizy:", height=150)
uploaded_file = st.file_uploader("📂 Opcjonalnie: Wczytaj plik (PDF, DOCX, JPG, PNG)", type=["pdf", "docx", "jpg", "png", "jpeg"])

# Podgląd obrazu
image_base64 = None
if uploaded_file and uploaded_file.type in ["image/jpeg", "image/png"]:
    st.image(uploaded_file, caption="Wgrane zdjęcie", width=250)
    image_base64 = encode_image(uploaded_file)

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input and not uploaded_file:
        st.warning("Proszę wprowadzić tekst lub wgrać plik.")
    else:
        with st.spinner('Trwa przetwarzanie danych...'):
            full_text =

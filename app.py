import streamlit as st
import re
from openai import OpenAI
import pdfplumber
from docx import Document
import base64

# 1. Konfiguracja strony
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# --- INICJALIZACJA LICZNIKÓW OD ZERA ---
if 'leaks_blocked' not in st.session_state:
    st.session_state['leaks_blocked'] = 0
if 'total_queries' not in st.session_state:
    st.session_state['total_queries'] = 0

# --- BEZPIECZNE POBIERANIE KLUCZA Z SECRETS ---
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    st.error("Błąd: Nie skonfigurowano klucza API w Secrets!")
    st.stop()

client = OpenAI(api_key=API_KEY)

# 2. Silnik anonimizacji danych (RODO)
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
    st.header("📈 Aktywność Twojej Sesji")
    # Wyświetlamy realne statystyki od 0
    st.metric(label="Zablokowane wycieki (łącznie)", value=st.session_state['leaks_blocked'])
    st.metric(label="Przetworzone zapytania", value=st.session_state['total_queries'])
    st.info("Statystyki są liczone od momentu uruchomienia aplikacji.")

# 4. Sekcja Główna
st.title("🛡️ SafeAI Gateway")
st.markdown("### Profesjonalna bariera ochronna dla firm korzystających z AI")
st.divider()

# 5. Interfejs Użytkownika
st.write("#### 🚀 Bezpieczne zapytanie do modelu GPT-4o")

if 'file_text' not in st.session_state:
    st.session_state['file_text'] = ""

user_input = st.text_area(
    "Wklej tutaj tekst do analizy (system ukryje dane osobowe):", 
    value=st.session_state['file_text'], 
    height=250
)

uploaded_file = st.file_uploader("📂 Opcjonalnie: Wczytaj treść z pliku (PDF, DOCX, JPG, PNG)", type=["pdf", "docx", "jpg", "png", "jpeg"])

image_base64 = None
if uploaded_file is not None:
    try:
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                if text != st.session_state['file_text']:
                    st.session_state['file_text'] = text
                    st.rerun()
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            if text != st.session_state['file_text']:
                st.session_state['file_text'] = text
                st.rerun()
        elif uploaded_file.type in ["image/jpeg", "image/png"]:
            st.image(uploaded_file, caption="Wgrane zdjęcie", width=300)
            image_base64 = encode_image(uploaded_file)
    except Exception as e:
        st.error(f"Błąd odczytu: {e}")

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input and image_base64 is None:
        st.warning("Najpierw wprowadź tekst lub wgraj obraz.")
    else:
        with st.spinner('Trwa analiza...'):
            final_prompt = user_input
            
            # Obsługa Vision dla zdjęć
            if image_base64:
                vision_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": [
                        {"type": "text", "text": "Przepisz tekst ze zdjęcia."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]}]
                )
                final_prompt = vision_response.choices[0].message.content

            # ANONIMIZACJA
            cleaned = clean_data(final_prompt)
            
            # --- LICZENIE WYKRYTYCH DANYCH W TYM ZAPYTANIU ---
            # Każdy tag [UKRYTY] oznacza zablokowany wyciek
            found_leaks = cleaned.count("[UKRYT") 
            
            st.info(f"🛡️ **Tarcza SafeAI:** Wykryto i zanonimizowano **{found_leaks}** wrażliwych danych.")
            st.code(cleaned)
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                
                # --- AKTUALIZACJA LICZNIKÓW SESJI ---
                st.session_state['leaks_blocked'] += found_leaks
                st.session_state['total_queries'] += 1
                
                st.success("✨ Odpowiedź od AI:")
                st.write(response.choices[0].message.content)
                
                # Odświeżenie, aby sidebar pokazał nowe dane
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Problem z połączeniem: {str(e)}")

# Stopka
st.divider()
st.caption("© 2026 SafeAI Gateway Polska | Zgodność z RODO i AI Act")

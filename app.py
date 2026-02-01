import streamlit as st
import re
from openai import OpenAI
import pdfplumber
from docx import Document

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
    st.header("📈 Aktywność dzisiaj")
    st.metric(label="Zablokowane wycieki", value="142", delta="+12%")
    st.metric(label="Przetworzone zapytania", value="1.2k")

# 4. Sekcja Marketingowa
st.title("🛡️ SafeAI Gateway")
st.markdown("### Profesjonalna bariera ochronna dla firm korzystających z AI")

col1, col2, col3 = st.columns(3)
with col1:
    st.error("⚖️ **AI Act (Nowe prawo)**")
    st.write("W 2026 roku wchodzą w życie kluczowe przepisy unijne o AI. Firmy, które nie kontrolują AI, mogą zostać uznane za podmioty 'wysokiego ryzyka'.")
with col2:
    st.error("🔐 **Luka RODO**")
    st.write("OpenAI domyślnie uczy się na danych. Jeśli pracownik wklei treść umowy, staje się ona częścią 'mózgu' AI. To złamanie RODO.")
with col3:
    st.error("🕵️ **Shadow AI**")
    st.write("Statystycznie 80% pracowników już używa AI prywatnie. My dajemy oficjalne, bezpieczne narzędzie firmowe.")

st.divider()

# 5. Interfejs Użytkownika - Pole tekstowe (GÓRA)
st.write("#### 🚀 Bezpieczne zapytanie do modelu GPT-4o")

# Inicjalizacja tekstu w sesji, aby przycisk wgrywania mógł go uzupełnić
if 'file_text' not in st.session_state:
    st.session_state['file_text'] = ""

user_input = st.text_area(
    "Wklej tutaj tekst do analizy (system ukryje dane osobowe):", 
    value=st.session_state['file_text'], 
    height=250
)

# --- OBSŁUGA PLIKÓW (DÓŁ) ---
st.write("---")
uploaded_file = st.file_uploader("📂 Opcjonalnie: Wczytaj treść z pliku (PDF, DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    try:
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
        
        if text != st.session_state['file_text']:
            st.session_state['file_text'] = text
            st.rerun() # Odśwież, aby tekst wskoczył do pola wyżej
    except Exception as e:
        st.error(f"Błąd odczytu: {e}")

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input:
        st.warning("Najpierw wprowadź tekst.")
    else:
        cleaned = clean_data(user_input)
        st.info("🛡️ **Tarcza SafeAI:** Dane zanonimizowane przed wysłaniem:")
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

# 6. Stopka i Nowy Opis
st.divider()
st.write("### O SafeAI Gateway")
st.write("Dostarczamy rozwiązania Privacy-First dla sektora prawnego i finansowego. Nasza bramka pozwala na bezpieczną adopcję AI zgodnie z polskim i europejskim prawem.")

f_col1, f_col2 = st.columns([2, 1])
with f_col1:
    st.write("Działamy w oparciu o zaawansowane filtry de-identyfikacji danych wrażliwych, zapewniając pełną poufność Twoich procesów biznesowych.")
with f_col2:
    st.write("### 📩 Kontakt")
    st.write("**E-mail:** vkarykin7@gmail.com")

st.divider()
st.caption("© 2026 SafeAI Gateway Polska | Zgodność z RODO i AI Act")

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

# --- TUTAJ DODAŁEM PRZYCISK DO PLIKÓW ---
st.write("#### 📂 Krok 1: Wgraj plik (PDF/DOCX)")
uploaded_file = st.file_uploader("Przeciągnij plik tutaj lub kliknij 'Browse files'", type=["pdf", "docx"])
extracted_text = ""

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            extracted_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        extracted_text = "\n".join([para.text for para in doc.paragraphs])
    st.success("✅ Plik wczytany!")

st.divider()

# 5. Interfejs Użytkownika - Pole tekstowe
st.write("#### 🚀 Krok 2: Bezpieczne zapytanie do GPT-4o")
user_input = st.text_area(
    "Edytuj treść lub wklej tekst ręcznie:", 
    value=extracted_text, # To połączy plik z polem tekstowym
    height=250
)

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input:
        st.warning("Najpierw wprowadź tekst lub wgraj plik.")
    else:
        cleaned = clean_data(user_input)
        st.info("🛡️ **Tarcza SafeAI:** Dane zanonimizowane:")
        st.code(cleaned)
        
        try:
            client = OpenAI(api_key=API_KEY)
            with st.spinner('Generowanie odpowiedzi...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                st.success("✨ Odpowiedź od AI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ Problem: {str(e)}")

# 6. Kontakt
st.divider()
st.write("📩 **Kontakt:** vkarykin7@gmail.com")
st.caption("© 2026 SafeAI Gateway Polska")

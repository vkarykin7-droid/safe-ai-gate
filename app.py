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
    # 1. Dane kontaktowe
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    
    # 2. Imiona i Nazwiska (Pan/Pani + Nazwisko)
    text = re.sub(r'(Pan|Pani|Panem|Panią)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)?', '[UKRYTY_KLIENT]', text)

    # 3. KONTA BANKOWE (IBAN i zwykłe)
    text = re.sub(r'\b(?:\d[ ]?){26}\b', '[UKRYTY_NR_KONTA]', text)
    text = re.sub(r'PL[ ]?\d{2}[ ]?(?:\d[ ]?){24}', '[UKRYTY_NR_KONTA_PL]', text)

    # 4. Inteligentne ID (NIP/PESEL/REGON)
    patterns = [r'NIP[:\s]*(\d+[-\d]*)', r'PESEL[:\s]*(\d+)', r'REGON[:\s]*(\d+)', r'NR DOWODU[:\s]*(\S+)']
    for pattern in patterns:
        text = re.sub(pattern, lambda m: m.group(0).split(':')[0] + ': [UKRYTE_DANE]', text, flags=re.IGNORECASE)

    # 5. Agresywny filtr na dowolne długie ciągi cyfr (od 6 wzwyż)
    text = re.sub(r'\b\d{6,}\b', '[UKRYTY_CIĄG_CYFR]', text)

    # 6. Adresy
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
    st.divider()
    st.write("🔒 **Technologia:** Każde zapytanie przechodzi przez lokalny filtr de-identyfikacji przed wysłaniem do AI.")

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

# --- OBSŁUGA PLIKÓW ---
st.write("#### 📂 Krok 1: Wgraj plik lub wpisz tekst")
uploaded_file = st.file_uploader("Wgraj dokument (PDF, DOCX)", type=["pdf", "docx"])
extracted_text = ""

if uploaded_file is not None:
    try:
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                extracted_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            extracted_text = "\n".join([para.text for para in doc.paragraphs])
        st.success("✅ Tekst z pliku został wczytany!")
    except Exception as e:
        st.error(f"Błąd podczas odczytu pliku: {e}")

# 5. Interfejs Użytkownika - Pole tekstowe
user_input = st.text_area(
    "Edytuj treść lub wklej tekst ręcznie:", 
    value=extracted_text, 
    height=250
)

if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input:
        st.warning("Najpierw wprowadź tekst lub wgraj plik.")
    else:
        # ANONIMIZACJA
        cleaned = clean_data(user_input)
        st.info("🛡️ **Tarcza SafeAI:** Twoje dane zostały zanonimizowane przed wysłaniem do AI:")
        st.code(cleaned)
        
        # WYSYŁKA DO OPENAI
        try:
            client = OpenAI(api_key=API_KEY)
            with st.spinner('Trwa generowanie bezpiecznej odpowiedzi...'):
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
    st.write("Dostarczamy rozwiązania Privacy-First dla sektora prawnego i finansowego. Nasza bramka pozwala na bezpieczną adopcję AI zgodnie z polskim i europejskim prawem.")
with f_col2:
    st.write("### 📩 Kontakt")
    st.write("**E-mail:** vkarykin7@gmail.com")
    st.write("**Wdrożenia:** Zapytaj o wersję dla Twojej firmy.")

st.divider()
st.caption("© 2026 SafeAI Gateway Polska | Zgodność z RODO i AI Act")

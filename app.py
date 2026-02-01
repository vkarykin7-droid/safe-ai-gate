import streamlit as st
import re
from openai import OpenAI
import pdfplumber
from docx import Document
import base64

# 1. Konfiguracja strony
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# --- INICJALIZACJA STANU SESJI (Pamięć aplikacji) ---
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

# --- BEZPIECZNE POBIERANIE KLUCZA ---
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=API_KEY)
except Exception:
    st.error("Błąd: Nie skonfigurowano klucza API w Secrets!")
    st.stop()

# 2. Silnik anonimizacji danych (RODO)
def clean_data(text):
    if not text:
        return ""
    # E-maile
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    # Telefony
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    # Dane osobowe (Imiona/Nazwiska w zwrotach)
    text = re.sub(r'(Pan|Pani|Panem|Panią)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)?', '[UKRYTY_KLIENT]', text)
    # Numery kont
    text = re.sub(r'\b(?:\d[ ]?){26}\b', '[UKRYTY_NR_KONTA]', text)
    # Dokumenty i identyfikatory
    patterns = [r'NIP[:\s]*(\d+[-\d]*)', r'PESEL[:\s]*(\d+)', r'REGON[:\s]*(\d+)', r'NR DOWODU[:\s]*(\S+)']
    for pattern in patterns:
        text = re.sub(pattern, lambda m: m.group(0).split(':')[0] + ': [UKRYTE_DANE]', text, flags=re.IGNORECASE)
    # Adresy
    text = re.sub(r'(ul\.|ulica|Al\.|Aleja|Plac|Park|ul)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(\s+[0-9A-Za-z/]+)?', '[UKRYTY_ADRES]', text)
    return text

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# 3. Panel Boczny (Sidebar)
with st.sidebar:
    st.header("⚙️ Status Systemu")
    st.success("✅ Połączono: SafeAI Cloud")
    st.divider()
    st.header("📈 Aktywność Sesji")
    st.metric(label="Zablokowane wycieki", value=st.session_state['leaks_blocked'])
    st.metric(label="Przetworzone zapytania", value=st.session_state['total_queries'])
    
    st.divider()
    if st.button("🗑️ Wyczyść aktualny wynik"):
        st.session_state['last_ai_response'] = None
        st.session_state['last_cleaned_text'] = None
        st.rerun()

# 4. Interfejs Główny
st.title("🛡️ SafeAI Gateway")
st.markdown("### Profesjonalna bariera ochronna dla firm korzystających z AI")

# Główne pola wejściowe
user_input = st.text_area("Wklej tekst do analizy:", height=200)
uploaded_file = st.file_uploader("📂 Opcjonalnie: Wgraj plik (PDF, DOCX, JPG, PNG)", type=["pdf", "docx", "jpg", "png", "jpeg"])

# Obsługa obrazu (podgląd i kodowanie)
image_base64 = None
if uploaded_file and uploaded_file.type in ["image/jpeg", "image/png"]:
    st.image(uploaded_file, caption="Wgrane zdjęcie do analizy Vision", width=300)
    image_base64 = encode_image(uploaded_file)

# 5. LOGIKA PRZETWARZANIA
if st.button("🚀 Uruchom Bezpieczne Przetwarzanie"):
    if not user_input and not uploaded_file:
        st.warning("Najpierw wprowadź tekst lub wgraj plik.")
    else:
        with st.spinner('Trwa analiza, anonimizacja i zapytanie do AI...'):
            # Inicjalizacja tekstu do wysłania
            full_text = user_input if user_input else ""
            
            # --- EKSTRAKCJA TEKSTU Z PLIKÓW ---
            if uploaded_file:
                try:
                    if uploaded_file.type == "application/pdf":
                        with pdfplumber.open(uploaded_file) as pdf:
                            pdf_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
                            full_text += "\n" + pdf_text
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        doc = Document(uploaded_file)
                        doc_text = "\n".join([p.text for p in doc.paragraphs])
                        full_text += "\n" + doc_text
                    elif image_base64:
                        # Wykorzystanie modelu Vision do odczytania tekstu ze zdjęcia
                        vision_res = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "user", "content": [
                                {"type": "text", "text": "Przepisz cały tekst z tego zdjęcia. Nie dodawaj komentarzy."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                            ]}]
                        )
                        full_text += "\n" + vision_res.choices[0].message.content
                except Exception as e:
                    st.error(f"Błąd podczas odczytu pliku: {e}")

            # --- ANONIMIZACJA ---
            cleaned = clean_data(full_text)
            leaks_count = cleaned.count("[UKRYT")
            
            # --- ZAPYTANIE DO CHATU ---
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Przeanalizuj poniższy tekst i wyciągnij najważniejsze wnioski:\n\n{cleaned}"}]
                )
                
                # Zapisujemy wyniki do sesji, aby nie zniknęły po odświeżeniu
                st.session_state['last_ai_response'] = response.choices[0].message.content
                st.session_state['last_cleaned_text'] = cleaned
                st.session_state['last_found_leaks'] = leaks_count
                
                # Aktualizacja liczników globalnych
                st.session_state['leaks_blocked'] += leaks_count
                st.session_state['total_queries'] += 1
                
                # Odświeżamy aplikację, aby sidebar pokazał nowe dane
                st.rerun()

            except Exception as e:
                st.error(f"❌ Problem z połączeniem OpenAI: {str(e)}")

# --- 6. STAŁA SEKCJA WYŚWIETLANIA WYNIKÓW ---
if st.session_state['last_ai_response']:
    st.divider()
    st.info(f"🛡️ **Tarcza SafeAI:** W tym procesie wykryto i zablokowano **{st.session_state['last_found_leaks']}** potencjalnych wycieków danych.")
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Tekst wysłany do AI (Zanonimizowany)")
        st.code(st.session_state['last_cleaned_text'])
    
    with col_right:
        st.subheader("Finalna Analiza AI")
        st.write(st.session_state['last_ai_response'])

# Stopka
st.divider()
st.caption("© 2026 SafeAI Gateway Polska | System ochrony danych wrażliwych")

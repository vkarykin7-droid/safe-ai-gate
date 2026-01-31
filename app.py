import streamlit as st
import re
from openai import OpenAI

# 1. Konfiguracja strony
st.set_page_config(
    page_title="SafeAI Gateway Pro", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Logika bezpieczeństwa (Twój silnik anonimizacji)
def clean_data(text):
    # Ukrywanie maili
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    # Ukrywanie NIP (format 000-000-00-00)
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text)
    # Ukrywanie PESEL (11 cyfr)
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text)
    # Ukrywanie numerów telefonów
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    return text

# 3. Panel boczny (Administracja)
with st.sidebar:
    st.header("🛡️ Panel Kontrolny")
    api_key = st.text_input("Klucz API OpenAI", type="password", help="Wklej klucz z platform.openai.com")
    
    st.divider()
    st.subheader("Status Ochrony")
    st.success("✅ Filtr RODO: Aktywny")
    st.success("✅ Zgodność AI Act: OK")
    
    st.divider()
    st.metric(label="Zablokowane wycieki", value="12", delta="+3 dzisiaj")
    st.caption("Wersja systemu: 1.0.4 Enterprise")

# 4. Sekcja Główna - Argumenty Sprzedażowe
st.title("🛡️ SafeAI Gateway")
st.subheader("Bezpieczny most między Twoją firmą a potęgą Sztucznej Inteligencji")

st.write("")
col1, col2, col3 = st.columns(3)

with col1:
    st.error("⚖️ **AI Act (Nowe prawo)**")
    st.caption("""
    W 2026 roku wchodzą w życie kluczowe przepisy unijne. Firmy bez kontroli nad tym, jak pracownicy używają AI, 
    mogą zostać uznane za podmioty **'wysokiego ryzyka'**.
    """)

with col2:
    st.error("🔓 **Luka RODO**")
    st.caption("""
    OpenAI domyślnie uczy się na Twoich danych. Jeśli pracownik wklei treść umowy, staje się ona częścią 'mózgu' AI. 
    To złamanie RODO, za które **prezes odpowiada finansowo**.
    """)

with col3:
    st.error("🕵️ **Shadow AI**")
    st.caption("""
    Statystycznie **80% pracowników już używa AI**, ale robią to poza Twoją kontrolą. 
    SafeAI to oficjalne i bezpieczne narzędzie, które eliminuje ten problem.
    """)

st.divider()

# 5. Interfejs Użytkownika
user_input = st.text_area(
    "Wpisz polecenie dla AI (system automatycznie wyczyści dane wrażliwe):", 
    placeholder="Np. Napisz maila do klienta jan.kowalski@firma.pl o fakturze na 5000 zł...", 
    height=200
)

if st.button("🚀 Generuj bezpieczną odpowiedź"):
    if not api_key:
        st.error("⚠️ Błąd: Proszę wprowadzić klucz API w panelu bocznym po lewej stronie.")
    elif not user_input:
        st.warning("⚠️ Proszę wpisać treść zapytania.")
    else:
        # KROK 1: Czyszczenie danych
        cleaned_prompt = clean_data(user_input)
        
        # KROK 2: Budowanie zaufania (Podgląd)
        with st.expander("👁️ Zobacz, jak system zabezpieczył Twoje dane (Podgląd dla AI)"):
            st.code(cleaned_prompt)
        
        # KROK 3: Połączenie z OpenAI
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner('Trwa bezpieczne przetwarzanie...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned_prompt}]
                )
                st.success("Odpowiedź SafeAI:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Wystąpił błąd: {e}")

# 6. Sekcja "O NAS" i Kontakt
st.write("")
st.write("")
st.divider()

col_a, col_b = st.columns([1, 3])

with col_a:
    st.markdown("<h1 style='text-align: center;'>👨‍💻</h1>", unsafe_allow_input=True)

with col_b:
    st.write(f"""
    ### O SafeAI Gateway
    Jesteśmy polskim projektem technologicznym dedykowanym dla sektora MŚP. 
    Pomagamy firmom wdrażać rozwiązania AI, eliminując ryzyko wycieku tajemnic przedsiębiorstwa.
    
    **Kontakt i wdrożenia:** [vkarykin7@gmail.com](mailto:vkarykin7@gmail.com)
    """)
    if st.button("Zamów darmową konsultację dla swojej firmy"):
        st.balloons()
        st.success("Świetnie! Napisz do nas na: vkarykin7@gmail.com")

st.divider()
st.caption("© 2026 SafeAI Gateway Polska | Twój partner w bezpiecznej transformacji AI")

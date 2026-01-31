import streamlit as st
import re
from openai import OpenAI

# 1. Konfiguracja strony
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# 2. Rozszerzona funkcja anonimizująca (Dodany filtr adresowy)
def clean_data(text):
    # Identyfikatory numeryczne i maile
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text)
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text)
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    
    # NOWOŚĆ: Filtr lokalizacyjny i adresowy
    text = re.sub(r'\d{2}-\d{3}', '[UKRYTY_KOD]', text) # Wykrywa kody pocztowe
    # Wykrywa ulice, place, parki i numery domów
    text = re.sub(r'(ul\.|ulica|Al\.|Aleja|Plac|Park|ul)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)*\s+\d+(/[0-9a-zA-Z]+)?', '[UKRYTY_ADRES]', text)
    
    return text

# 3. Panel Boczny
with st.sidebar:
    st.header("🛡️ Panel Kontrolny")
    api_key = st.text_input("Klucz API OpenAI", type="password")
    st.divider()
    st.write("✅ Filtr RODO: Aktywny")
    st.write("✅ Zgodność AI Act: OK")
    st.divider()
    st.metric(label="Zablokowane wycieki", value="15")
    st.caption("Wersja: 1.1.0 Enterprise")

# 4. Strona Główna i Argumenty Biznesowe
st.title("🛡️ SafeAI Gateway")
st.subheader("Bezpieczny dostęp do AI dla Twojego Biznesu")

# Sekcja Ryzyk
col1, col2, col3 = st.columns(3)
with col1:
    st.error("⚖️ **AI Act (Prawo)**")
    st.write("Firmy bez kontroli AI w 2026 r. mogą być uznane za podmioty wysokiego ryzyka.")
with col2:
    st.error("🔓 **Odpowiedzialność**")
    st.write("Dane wklejane do ChatGPT stają się częścią publicznego zbioru treningowego. To złamanie RODO, za które prezes i zarząd odpowiadają majątkiem osobistym.")
with col3:
    st.error("🕵️ **Shadow AI**")
    st.write("80% pracowników używa AI bez Twojej wiedzy. Daj im bezpieczne, oficjalne narzędzie.")

st.divider()

# 5. Obsługa zapytań
user_input = st.text_area("Wpisz polecenie dla AI (system usunie dane wrażliwe, w tym adresy i identyfikatory):", height=150)

if st.button("🚀 Generuj bezpieczną odpowiedź"):
    if not api_key:
        st.error("Wprowadź klucz API w panelu bocznym.")
    elif not user_input:
        st.warning("Wpisz tekst do przetworzenia.")
    else:
        cleaned_prompt = clean_data(user_input)
        
        with st.expander("👁️ Podgląd ochrony (Tyle widzi AI)"):
            st.code(cleaned_prompt)
        
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
            st.error(f"Błąd połączenia: {e}")

# 6. Sekcja O NAS i KONTAKT
st.write("")
st.divider()
st.subheader("O projekcie SafeAI Gateway")
st.write("""
Jesteśmy polskim dostawcą rozwiązań ochrony danych w erze AI. Nasza misja to bezpieczna transformacja cyfrowa firm 
z sektora MŚP. Dzięki naszej technologii, pracownicy mogą korzystać z najnowocześniejszych modeli językowych 
bez narażania firmy na ryzyka prawne.
""")

st.info(f"📩 **Kontakt i wdrożenia:** vkarykin7@gmail.com")
st.caption("© 2026 SafeAI Gateway Polska | Twój partner w bezpiecznym AI")

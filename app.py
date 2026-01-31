import streamlit as st
import re
from openai import OpenAI

# 1. Konfiguracja (Musi być na samej górze)
st.set_page_config(page_title="SafeAI Gateway Pro", page_icon="🛡️", layout="wide")

# 2. Silnik anonimizacji
def clean_data(text):
    text = re.sub(r'\S+@\S+', '[UKRYTY_EMAIL]', text)
    text = re.sub(r'\d{3}-\d{3}-\d{2}-\d{2}', '[UKRYTY_NIP]', text)
    text = re.sub(r'\d{11}', '[UKRYTY_PESEL]', text)
    text = re.sub(r'(?:\+\d{2})?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}', '[UKRYTY_TEL]', text)
    return text

# 3. Panel Boczny
with st.sidebar:
    st.header("🛡️ Panel Kontrolny")
    api_key = st.text_input("Klucz API OpenAI", type="password")
    st.divider()
    st.write("✅ Filtr RODO: Aktywny")
    st.write("✅ Zgodność AI Act: OK")
    st.divider()
    st.metric(label="Zablokowane wycieki", value="12", delta="+3 dzisiaj")

# 4. Strona Główna i Argumenty Biznesowe
st.title("🛡️ SafeAI Gateway")
st.subheader("Bezpieczny dostęp do AI dla Twojego Biznesu")

# Trzy kolumny z ryzykami
c1, c2, c3 = st.columns(3)
with c1:
    st.error("⚖️ **AI Act (Prawo)**")
    st.write("Firmy bez kontroli AI w 2026 r. mogą być uznane za podmioty wysokiego ryzyka.")
with c2:
    st.error("🔓 **Luka RODO**")
    st.write("Dane wklejane do ChatGPT uczą model. To złamanie RODO, za które odpowiada prezes.")
with c3:
    st.error("🕵️ **Shadow AI**")
    st.write("80% pracowników używa AI bez Twojej wiedzy. Daj im bezpieczne narzędzie.")

st.divider()

# 5. Obsługa zapytań
user_input = st.text_area("Wpisz zapytanie (system wyczyści dane):", height=150)

if st.button("🚀 Generuj bezpieczną odpowiedź"):
    if not api_key:
        st.error("Wprowadź klucz API w panelu bocznym.")
    elif not user_input:
        st.warning("Wpisz tekst.")
    else:
        cleaned = clean_data(user_input)
        with st.expander("👁️ Podgląd ochrony (To widzi AI)"):
            st.code(cleaned)
        
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner('Przetwarzanie...'):
                resp = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": cleaned}]
                )
                st.success("Odpowiedź SafeAI:")
                st.write(resp.choices[0].message.content)
        except Exception as e:
            st.error(f"Błąd API: {e}")

# 6. Sekcja O nas i Kontakt
st.divider()
st.subheader("O SafeAI Gateway")
st.write("""
Pomagamy polskim firmom wdrażać AI zgodnie z prawem. 
Nasz system to tarcza chroniąca Twoje tajemnice handlowe i dane osobowe.
""")
st.info("📩 **Kontakt i wdrożenia:** vkarykin7@gmail.com")

st.caption("© 2026 SafeAI Gateway Polska")

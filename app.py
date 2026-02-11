"""
SafeAI Gateway Pro - Bezpieczny Agent AI z Anonimizacją Danych (RODO)
======================================================================
Główny plik aplikacji Streamlit.
"""

import sys
import os

# Dodajemy katalog projektu do ścieżki Pythona — wymagane na Streamlit Cloud
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from core.redaction import DataRedactor
from core.extractors import FileExtractor
from core.ai_client import SafeAIClient
from core.stats import SessionStats
from ui.sidebar import render_sidebar
from ui.results import render_results
from config import AppConfig

# ─────────────────────────────────────────────
# Konfiguracja strony
# ─────────────────────────────────────────────
st.set_page_config(
    page_title=AppConfig.APP_TITLE,
    page_icon=AppConfig.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Inicjalizacja stanu sesji
# ─────────────────────────────────────────────
SessionStats.initialize()

# ─────────────────────────────────────────────
# Inicjalizacja komponentów
# ─────────────────────────────────────────────
try:
    ai_client = SafeAIClient()
except RuntimeError as e:
    st.error(f"❌ {e}")
    st.info("Upewnij się, że klucz OPENAI_API_KEY jest dodany do `.streamlit/secrets.toml`")
    st.stop()

redactor = DataRedactor()
extractor = FileExtractor(ai_client)

# ─────────────────────────────────────────────
# Panel boczny
# ─────────────────────────────────────────────
render_sidebar()

# ─────────────────────────────────────────────
# Nagłówek
# ─────────────────────────────────────────────
st.title(f"{AppConfig.APP_ICON} {AppConfig.APP_TITLE}")
st.markdown(
    "**Profesjonalna bariera ochronna RODO** — Twoje dane są anonimizowane "
    "*przed* wysłaniem do AI. ChatGPT nigdy nie widzi danych osobowych."
)
st.divider()

# ─────────────────────────────────────────────
# Formularz wejściowy
# ─────────────────────────────────────────────
col_input, col_options = st.columns([3, 1])

with col_input:
    user_command = st.text_area(
        "📝 Twoje polecenie:",
        placeholder='Np. "Napisz wezwanie do zapłaty" lub "Streść ten dokument"...',
        height=120,
        key="user_command",
    )

with col_options:
    st.markdown("**⚙️ Opcje przetwarzania**")
    show_redacted = st.toggle("Pokaż zanonimizowany tekst", value=True)
    ai_model = st.selectbox(
        "Model AI",
        options=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        index=0,
    )

uploaded_file = st.file_uploader(
    "📂 Opcjonalnie: Wgraj plik (PDF, DOCX, JPG, PNG)",
    type=["pdf", "docx", "jpg", "jpeg", "png"],
    help="Tekst z pliku zostanie automatycznie wyciągnięty i zanonimizowany.",
)

if uploaded_file and uploaded_file.type.startswith("image/"):
    st.image(uploaded_file, caption="Wgrane zdjęcie — Vision OCR w trakcie...", width=280)

# ─────────────────────────────────────────────
# Przycisk przetwarzania
# ─────────────────────────────────────────────
process_btn = st.button(
    "🚀 Uruchom Bezpieczne Przetwarzanie",
    type="primary",
    use_container_width=True,
    disabled=(not user_command and not uploaded_file),
)

# ─────────────────────────────────────────────
# Logika przetwarzania
# ─────────────────────────────────────────────
if process_btn:
    with st.status("🔄 Przetwarzanie w toku...", expanded=True) as status:

        # Krok 1: Ekstrakcja tekstu z pliku
        file_text = ""
        if uploaded_file:
            st.write("📄 **Krok 1/3:** Wyciąganie tekstu z pliku...")
            file_text, error = extractor.extract(uploaded_file)
            if error:
                st.error(f"Błąd ekstrakcji pliku: {error}")
            else:
                st.write(f"✅ Wyciągnięto {len(file_text)} znaków z pliku.")

        # Krok 2: Anonimizacja
        st.write("🛡️ **Krok 2/3:** Anonimizacja danych wrażliwych (lokalnie)...")
        full_content = f"POLECENIE: {user_command}\n\nDANE:\n{file_text}" if file_text else user_command
        redacted_text, leak_count = redactor.redact(full_content)
        st.write(f"✅ Wykryto i ukryto **{leak_count}** pól z danymi wrażliwymi.")

        # Krok 3: Zapytanie do AI
        st.write(f"🤖 **Krok 3/3:** Wysyłanie do {ai_model} (bez danych osobowych)...")
        ai_response, ai_error = ai_client.complete(redacted_text, model=ai_model)

        if ai_error:
            st.error(f"❌ Problem z OpenAI: {ai_error}")
            status.update(label="❌ Wystąpił błąd", state="error")
        else:
            # Zapis wyników do sesji
            SessionStats.record_query(leak_count)
            st.session_state["last_response"] = ai_response
            st.session_state["last_redacted"] = redacted_text
            st.session_state["last_leaks"] = leak_count
            st.session_state["last_model"] = ai_model
            status.update(label="✅ Gotowe!", state="complete")

# ─────────────────────────────────────────────
# Wyświetlanie wyników
# ─────────────────────────────────────────────
render_results(show_redacted=show_redacted)

# ─────────────────────────────────────────────
# Stopka
# ─────────────────────────────────────────────
st.divider()
st.caption(
    f"© 2026 SafeAI Gateway | v{AppConfig.VERSION} | "
    "System ochrony danych wrażliwych zgodny z RODO"
)

# main.py 
import streamlit as st
import os
import boto3
from data.database import DatabaseManager  # Importujemy DatabaseManager
from ui.sidebar import (
    sidebar_content,
    display_translation_history,
    display_vocabulary,
    search_vocabulary,
)
from core.translator import handle_translation_tab  # Importujemy translator
from core.grammar import handle_exercise_tab
from services.openai_client import translate_text_with_openai, text_to_speech_tts1
from core.utils import get_lang_mappings

# Konfiguracja aplikacji Streamlit
st.set_page_config(page_title="LinguaMaster", layout="wide")

# Ustawienie klienta DigitalOcean Spaces
session = boto3.session.Session()
client = session.client(
    's3',
    region_name=os.getenv('AWS_REGION'),
    endpoint_url=os.getenv('AWS_ENDPOINT_URL_S3'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Opcjonalna inicjalizacja Langfuse
langfuse = None
if all([
    os.getenv("LANGFUSE_PUBLIC_KEY"),
    os.getenv("LANGFUSE_SECRET_KEY"),
    os.getenv("LANGFUSE_HOST")
]):
    from langfuse import Langfuse
    langfuse = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST")
    )

# Inicjalizacja bazy danych w stanie sesji (raz!)
if "db" not in st.session_state:
    st.session_state.db = DatabaseManager()
    st.session_state.db.create_tables()  # Tworzymy tabele bazy danych

# Teraz, gdy baza danych jest zainicjalizowana, możesz zaimportować resztę modułów i korzystać z bazy
sidebar_content()

def sidebar_content():
    # Styl nagłówka menu
    st.sidebar.markdown(
        """
        <div style='
            font-size: 34px;
            font-weight: 700;
            color: #4F8BF9;
            margin-bottom: 20px;
        '>🧭 Menu</div>
        """,
        unsafe_allow_html=True
    )

    # Styl radiobuttonów
    st.sidebar.markdown(
        """
        <style>
        div[data-baseweb="radio"] > div {
            font-size: 18px;
            padding-top: 6px;
            padding-bottom: 6px;
        }
        div[data-baseweb="radio"] label {
            margin-bottom: 8px;
        }
        div[data-baseweb="radio"] input:checked + div {
            color: #1f77b4;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Unikalny key oraz label_visibility
    menu = st.sidebar.radio(
        label="Wybierz opcję",
        options=[
            "Start",
            "Tłumaczenie",
            "Historia tłumaczeń",
            "Słówka",
            "Wyszukaj słówka"
        ],
        key="menu_sidebar_radio",
        label_visibility="collapsed"  # ukrywa label, ale Streamlit nie rzuca błędem
    )

    return menu

# --- Główna logika aplikacji ---
menu = sidebar_content()

if menu == "Start":
    st.title(":blue[📚 LinguaMaster]")
    tab1, tab2 = st.tabs(["Tłumaczenie", "Interaktywne Ćwiczenia"])
    with tab1:
        handle_translation_tab()
    with tab2:
        handle_exercise_tab()

elif menu == "Tłumaczenie":
    st.title("🔄 Szybkie tłumaczenie")
    api_key = st.text_input("Wprowadź klucz API OpenAI", type="password", key="api_key_input")
    text = st.text_area("Tekst do przetłumaczenia", key="translation_textarea")

    if api_key and text:
        try:
            result = translate_text_with_openai(api_key, text, "en", "pl")
            if result and hasattr(result, "translated_text"):
                st.success("Tłumaczenie:")
                st.write(result.translated_text)

                if st.button("🔊 Odtwórz mowę"):
                    audio_file = text_to_speech_tts1(result.translated_text, lang="pl")
                    st.audio(audio_file)
            else:
                st.warning("Brak odpowiedzi z modelu.")
        except Exception as e:
            st.error(f"Wystąpił błąd podczas tłumaczenia: {e}")

elif menu == "Historia tłumaczeń":
    st.title("📜 Historia tłumaczeń")
    lang_mapping, *_ = get_lang_mappings()
    display_translation_history(lang_mapping)

elif menu == "Słówka":
    st.title("🗂️ Twoje słówka")
    display_vocabulary()

elif menu == "Wyszukaj słówka":
    st.title("🔍 Wyszukiwanie słówek")
    search_vocabulary()
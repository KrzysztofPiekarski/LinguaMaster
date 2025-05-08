
import streamlit as st
from data.database import DatabaseManager
from core.utils import get_lang_mappings
from services.openai_client import (
    translate_text_with_openai,
    text_to_speech_tts1,
    get_grammar_tips,
    generate_grammar_quiz,
)

def get_db():
    """Zwraca instancję bazy danych z sesji, jeśli jest zainicjalizowana, lub ją inicjalizuje."""
    if "db" not in st.session_state:
        st.session_state.db = DatabaseManager()
        st.session_state.db.create_tables()  # Tworzymy tabele bazy danych, jeśli jeszcze nie istnieją
    return st.session_state.db

def handle_translation_tab():
    db = get_db()  # Uzyskujemy dostęp do zainicjalizowanej bazy danych
    lang_mapping, lang_mapping2, _ = get_lang_mappings()

    api_key = st.text_input("Wprowadź swój klucz API OpenAI", type="password")

    c1, c2 = st.columns(2)
    with c1:
        src_lang = st.selectbox("Język źródłowy", list(lang_mapping.keys()))
    with c2:
        dest_lang = st.selectbox("Język docelowy", list(lang_mapping2.keys()))

    text = st.text_area("Wprowadź tekst do przetłumaczenia", max_chars=300)

    if st.button("🔠🔁 Tłumacz"):
        if not api_key or not text:
            st.info("Wprowadź klucz API i tekst.")
        else:
            try:
                translation = translate_text_with_openai(api_key, text, src_lang, dest_lang)
                st.session_state.translated_text = translation.translated_text
                db.insert_translation(text, translation.translated_text, src_lang, dest_lang)
                st.session_state.audio = text_to_speech_tts1(translation.translated_text)
            except Exception as e:
                st.error(str(e))
            translation = translate_text_with_openai(api_key, text, src_lang, dest_lang)
            st.session_state.translated_text = translation.translated_text

            db.insert_translation(text, translation.translated_text, src_lang, dest_lang)  # Używamy metody insert_translation
            st.session_state.audio = text_to_speech_tts1(translation.translated_text)

    if "translated_text" in st.session_state:
        st.subheader(":red[Przetłumaczone tekst]")
        st.write(st.session_state.translated_text)
        if st.session_state.audio:
            st.audio(st.session_state.audio)

    if api_key and "translated_text" in st.session_state:
        if st.button("📝💡 Pokaż wskazówki gramatyczne"):
            tips = get_grammar_tips(api_key, text, st.session_state.translated_text, src_lang, dest_lang)
            st.session_state.grammar_tips = tips
            st.rerun()

    if "grammar_tips" in st.session_state:
        st.write(st.session_state.grammar_tips)

    if st.button("🧠🎮 Generuj quiz"):
        quiz = generate_grammar_quiz(st.session_state.translated_text)
        for q in quiz:
            st.write(q)

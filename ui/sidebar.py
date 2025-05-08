import streamlit as st
from core.utils import get_lang_mappings
from core.translator import handle_translation_tab
from core.grammar import handle_exercise_tab
from services.openai_client import translate_text_with_openai, text_to_speech_tts1
from data.database import DatabaseManager

 # Inicjalizacja bazy danych
if "db" not in st.session_state:
        st.session_state.db = DatabaseManager()
        st.session_state.db.create_tables()

def sidebar_content():
    """Generuje zawartość bocznego panelu Streamlit z niestandardowym stylem"""

    # Stylowany tytuł sidebaru
    st.sidebar.markdown(
        """
        <div style='
            font-size: 34px;
            font-weight: 700;
            color: #4a90e2;
            margin-bottom: 0px;
        '>🎓🧠 Menu</div>
        """,
        unsafe_allow_html=True
    )

    # Stylowane etykiety przycisków
    st.sidebar.markdown(
        """
        <style>
        .sidebar-radio label {
            font-size: 18px !important;
            margin-bottom: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Opakowanie radio w dodatkowy znacznik klasy (dla CSS powyżej)
    menu = st.sidebar.radio(
        " ",
        ["Start", "Tłumaczenie", "Historia tłumaczeń", "Słówka do zapamiętania", "Wyszukaj słówka"],
        key="menu_radio"
    )

    # Pobieranie mapowań języków
    lang_mapping, lang_mapping2, lang_mapping3 = get_lang_mappings()

    # Logika dla wybranego menu
    if menu == "Start":
        st.title(":blue[📚 LinguaMaster]")
        tab1, tab2 = st.tabs(["Tłumaczenie", "Interaktywne Ćwiczenia"])
        with tab1:
            handle_translation_tab()
        with tab2:
            handle_exercise_tab()

    elif menu == "Tłumaczenie":
        st.title("🌍💬 Szybkie tłumaczenie")
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
        st.title("🕒📜 Historia tłumaczeń")
        display_translation_history(lang_mapping)

    elif menu == "Słówka do zapamiętania":
        st.title("🧠💡 Słówka do zapamiętania")

        # Formularz dodawania nowego słowa
        col1, col2, col3 = st.columns(3)
        with col1:
            new_word = st.text_input("Nowe słowo", key="new_word_input")
        with col2:
            new_translation = st.text_input("Tłumaczenie", key="new_translation_input")
        with col3:
            new_lang = st.selectbox(
                "Język", list(lang_mapping3.keys()), key="new_lang_select"
            )

        if st.button("Dodaj słowo"):
            if new_word and new_translation:
                st.session_state.db.insert_vocabulary(new_word, new_translation, new_lang)  # Używamy db
                st.success(f"'{new_word}' dodano do słówek do zapamiętania.")
                st.rerun()
            else:
                st.warning("Proszę wypełnić wszystkie pola.")

        # Wyświetlanie słówek do zapamiętania
        vocabulary = st.session_state.db.get_vocabulary()  # Używamy db
        for idx, word_data in enumerate(vocabulary):
            word, translation, lang = word_data[1], word_data[2], word_data[3]
            st.write(f"{word} -> {translation} ({lang})")
            if st.button(
                f"Usuń {word} -> {translation}", key=f"vocab_{word_data[0]}_{idx}"
            ):
                st.session_state.db.delete_vocabulary(word_data[0])  # Używamy db
                st.success(f"'{word}' zostało usunięte.")
                st.rerun()

    elif menu == "Wyszukaj słówka":
        st.title("🔎📝 Wyszukiwanie słówek")
        search_vocabulary()

def display_translation_history(lang_mapping, limit=None):
    """Wyświetla historię tłumaczeń w głównym panelu aplikacji"""
    db = st.session_state.db

    # Suwak do wyboru liczby tłumaczeń
    if limit is None:
        limit = st.slider("Liczba tłumaczeń do wyświetlenia", min_value=1, max_value=50, value=5)

    history = db.get_translation_history(limit=limit)

    st.markdown("### Historia tłumaczeń")

    if history:
        for entry in history:
            st.write(f"**{entry[1]}** → **{entry[2]}**  \n(_{entry[3]} → {entry[4]}_)")
    else:
        st.info("Brak historii tłumaczeń.")

def display_vocabulary():
    """Wyświetla słówka"""
    db = st.session_state.db
    vocabulary = db.get_vocabulary()
    if vocabulary:
        for entry in vocabulary:
            st.sidebar.write(f"{entry[1]} → {entry[2]} ({entry[3]})")
    else:
        st.sidebar.info("Brak słówek.")

def search_vocabulary():
    """Generuje wyszukiwanie słówek"""
    st.sidebar.subheader("Wyszukaj słówko")
    query = st.sidebar.text_input("Wpisz słowo lub tłumaczenie", key="search_input")

    if query:
        db = st.session_state.db
        results = db.search_vocabulary(query)
        if results:
            for _, word, translation, lang in results:
                st.sidebar.write(f"**{word}** → {translation} ({lang})")
        else:
            st.sidebar.info("Brak wyników.")

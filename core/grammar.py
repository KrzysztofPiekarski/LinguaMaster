import streamlit as st
from services.openai_client import analyze_user_text, generate_random_words
from core.utils import get_lang_mappings

def handle_exercise_tab():
    # Pobierz mapowanie języków
    lang_mapping, lang_mapping2, lang_mapping3 = get_lang_mappings()  # Rozpakuj krotkę na trzy zmienne

    # Wybór języka
    dest_lang = st.selectbox("Wybierz język", list(lang_mapping3.keys()))  # Użyj lang_mapping3

    # Wprowadzenie klucza API
    api_key = st.text_input("Wprowadź klucz API OpenAI", type="password")  # Klucz API

    # Jeśli nie ma losowych słów w sesji, generuj je
    if "random_words" not in st.session_state:
        if api_key:
            st.session_state.random_words = generate_random_words(dest_lang, api_key)  # Przekazanie api_key
        else:
            st.error("Klucz API jest wymagany.")
            return

    # Wyświetlanie losowych słów w zdaniu
    st.write("Użyj słów w zdaniu:")
    st.write(", ".join(st.session_state.random_words))

    # Przyciski do losowania nowych słów
    if st.button("Losuj 🎲"):
        if api_key:
            st.session_state.random_words = generate_random_words(dest_lang, api_key)  # Przekazanie api_key
            st.rerun()  # Odświeżenie strony, aby pokazać nowe słowa
        else:
            st.error("Klucz API jest wymagany.")
            return

    # Wprowadzenie zdania do analizy
    user_sentence = st.text_input("Twoje zdanie:", key="user_sentence")
    if st.button("Sprawdź zdanie") and user_sentence.strip():
        feedback = analyze_user_text(api_key, user_sentence)
        st.write(feedback)

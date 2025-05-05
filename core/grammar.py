import streamlit as st
from services.openai_client import analyze_user_text, generate_random_words
from core.utils import get_lang_mappings
import openai

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

    if st.button("Sprawdź zdanie"):
        if not api_key:
            st.error("Klucz API jest wymagany.")
        elif user_sentence.strip():
            feedback = analyze_user_text(api_key, user_sentence)
            st.subheader("📋 Analiza tekstu")
            st.write(feedback)
        else:
            st.warning("⚠️ Proszę wprowadzić zdanie.")
    
    # --- Dodany chatbot językowy ---
    st.markdown("---")  # Separator
    handle_chatbot(api_key)


def handle_chatbot(api_key: str):
    st.subheader("Asystent językowy 🤖")

    user_input = st.text_input("Wprowadź wiadomość do chatbota:", key="chatbot_input")

    if not api_key:
        st.info("Podaj klucz API, aby korzystać z asystenta.")
        return

    if user_input and st.button("Wyślij"):
        conversation_messages = [
            {
                "role": "system",
                "content": "Jesteś ekspertem do spraw językowych. Znasz wszystkie języki świata i udzielasz kompleksowych porad oraz odpowiedzi na pytania użytkownika.",
            },
            {"role": "user", "content": user_input},
        ]

        # UTWÓRZ klienta z kluczem API
        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_messages,
            max_tokens=300,
        )

        chatbot_reply = response.choices[0].message.content.strip()
        st.write(chatbot_reply)

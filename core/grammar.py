import streamlit as st
from services.openai_client import analyze_user_text, generate_random_words
from core.utils import get_lang_mappings
import streamlit.components.v1 as components
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
    if st.button("🎲 Losuj"):
        if api_key:
            st.session_state.random_words = generate_random_words(dest_lang, api_key)  # Przekazanie api_key
            st.rerun()  # Odświeżenie strony, aby pokazać nowe słowa
        else:
            st.error("Klucz API jest wymagany.")
            return

    # Wprowadzenie zdania do analizy
    user_sentence = st.text_input("Twoje zdanie:", key="user_sentence")

    if st.button("🔍 Sprawdź zdanie"):
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

def scroll_to_bottom():
    """Automatyczne przewinięcie do dołu."""
    scroll_script = """
    <script>
        var body = window.parent.document.querySelector(".main");
        body.scrollTo({top: body.scrollHeight, behavior: "smooth"});
    </script>
    """
    components.html(scroll_script, height=0)

def handle_chatbot(api_key: str):
    st.subheader("🧠🗣️ Asystent językowy")

    if not api_key:
        st.info("Podaj klucz API, aby korzystać z asystenta.")
        return

    # Inicjalizacja historii
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "last_user_input" not in st.session_state:
        st.session_state.last_user_input = None

    # Przycisk czyszczenia rozmowy
    if st.button("🧹 Wyczyść rozmowę"):
        st.session_state.chat_history = []
        st.session_state.last_user_input = None
        st.rerun()

    # Wyświetl historię
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Jeśli jest nowe zapytanie z poprzedniego przebiegu, generujemy odpowiedź
    if st.session_state.last_user_input:
        with st.chat_message("user"):
            st.markdown(st.session_state.last_user_input)

        # Przygotuj dane do API
        messages = [
            {"role": "system", "content": "Jesteś ekspertem językowym. Odpowiadasz jasno, konkretnie i zrozumiale."}
        ] + st.session_state.chat_history + [
            {"role": "user", "content": st.session_state.last_user_input}
        ]

        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=300,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"⚠️ Wystąpił błąd: {e}"

        st.session_state.chat_history.append({"role": "user", "content": st.session_state.last_user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.session_state.last_user_input = None

        with st.chat_message("assistant"):
            st.markdown(reply)

        scroll_to_bottom()
        st.rerun()

    # Pole na nową wiadomość (na samym dole)
    user_input = st.chat_input("Zadaj kolejne pytanie")

    if user_input:
        st.session_state.last_user_input = user_input
        st.rerun()

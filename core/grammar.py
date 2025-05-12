import streamlit as st
import streamlit.components.v1 as components
import openai
from services.openai_client import analyze_user_text, generate_random_words
from core.utils import get_lang_mappings

def handle_exercise_tab(api_key: str):
    if not api_key:
        st.error("❌ Brakuje klucza API OpenAI. Podaj go w panelu bocznym.")
        return

    # Pobierz mapowanie języków
    lang_mapping, lang_mapping2, lang_mapping3 = get_lang_mappings()

    # Wybór języka
    dest_lang = st.selectbox("Wybierz język", list(lang_mapping3.keys()), key="dest_lang")

    # Wybór liczby słów do wylosowania
    num_words = st.slider("Ile słów chcesz wylosować?", min_value=3, max_value=10, value=5, step=1, key="num_words")

    # Inicjalizacja słów przy pierwszym uruchomieniu lub po zmianie języka
    if (
        "random_words_initialized" not in st.session_state 
        or st.session_state.get("last_lang") != dest_lang 
        or st.session_state.get("last_num_words") != num_words
    ):
        st.session_state.random_words = generate_random_words(dest_lang, num_words=num_words)
        st.session_state.random_words_initialized = True
        st.session_state.last_lang = dest_lang
        st.session_state.last_num_words = num_words
        st.session_state.user_sentence = ""

    # 🧭 Instrukcja dla użytkownika przed sprawdzeniem zdania
    if not st.session_state.get("user_sentence"):
        st.info("✍️ Najpierw wpisz zdanie z użyciem powyższych słów i kliknij „🔍 Sprawdź zdanie”. Dopiero potem możesz losować kolejne.")

    # Przycisk do losowania nowych słów
    if st.button("🎲 Losuj"):
        st.session_state.random_words = generate_random_words(dest_lang, num_words=num_words)
        st.session_state.user_sentence = ""

    # Wyświetl wylosowane słowa
    if st.session_state.get("random_words"):
        st.write("Użyj słów w zdaniu:")
        formatted_words = [f"{word} ({translation})" for word, translation in st.session_state.random_words]
        st.write(", ".join(formatted_words))

    # Pole tekstowe
    user_sentence = st.text_input("Twoje zdanie:", key="user_sentence")

    # Sprawdzenie zdania
    if st.button("🔍 Sprawdź zdanie"):
        if user_sentence.strip():
            feedback = analyze_user_text(api_key, user_sentence)
            st.subheader("Analiza tekstu")
            st.write(feedback)
        else:
            st.warning("Proszę wprowadzić zdanie.")

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
    if not api_key:
        st.error("❌ Brakuje klucza API OpenAI. Podaj go w panelu bocznym.")
        return

    st.subheader("🧠🗣️ Asystent językowy")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "last_user_input" not in st.session_state:
        st.session_state.last_user_input = None

    # Przycisk czyszczenia rozmowy
    if st.button("🧹 Wyczyść rozmowę"):
        st.session_state.chat_history = []
        st.session_state.last_user_input = None
        st.rerun()

    # Wyświetlenie historii
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Obsługa zapytania z poprzedniego przebiegu
    if st.session_state.last_user_input:
        with st.chat_message("user"):
            st.markdown(st.session_state.last_user_input)

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

    # Pole do wpisania nowej wiadomości
    user_input = st.chat_input("Zadaj kolejne pytanie")

    if user_input:
        st.session_state.last_user_input = user_input
        st.rerun()

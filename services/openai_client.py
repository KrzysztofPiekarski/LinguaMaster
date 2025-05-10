from pydantic import BaseModel
from langfuse.decorators import observe
from io import BytesIO
import openai
import random

# klasa Translation
class Translation(BaseModel):
    translated_text: str
    language: str

@observe()
# Funkcja do tłumaczenia tekstu za pomocą AI
def translate_text_with_openai(api_key, text, src_lang, dest_lang):
    openai.api_key = api_key
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Jesteś profesjonalnym tłumaczem."},
            {
                "role": "user",
                "content": f"Przetłumacz ten tekst bez żadnych komentarzy z {src_lang} na {dest_lang}: {text}.",
            },
        ],
        max_tokens=500,
    )
    translated_text = response.choices[0].message.content.strip()
    return Translation(translated_text=translated_text, language=dest_lang)


def text_to_speech_tts1(text):
    response = openai.audio.speech.create(
        model="tts-1",
        input=text,
        voice="alloy",
    )
    audio_content = response.content
    audio = BytesIO(audio_content)
    audio.seek(0)

    return audio

@observe()
# Funkcja do uzyskiwania wskazówek gramatycznych od AI
def get_grammar_tips(api_key, src_text, translated_text, src_lang, dest_lang):
    openai.api_key = api_key
    messages = [
        {"role": "system", "content": "Jesteś ekspertem od gramatyki."},
        {
            "role": "user",
            "content": f"Podaj wskazówki gramatyczne dla następującego tłumaczenia:\n\nOryginał ({src_lang}): {src_text}\nPrzetłumaczone ({dest_lang}): {translated_text}\n\nWyjaśnij kluczowe różnice gramatyczne.",
        },
    ]
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        # max_tokens=500,
        stream=True,
    )
    return response


@observe
def analyze_user_text(api_key, user_text):
    try:
        openai.api_key = api_key
        messages = [
            {
                "role": "system",
                "content": (
                    "Jesteś ekspertem językowym znającym wszystkie języki świata. "
                    "Twoim zadaniem jest analizować teksty pod względem gramatyki, składni i poprawności językowej. "
                    "Podawaj konkretne błędy oraz krótkie sugestie jak poprawić tekst. "
                    "Odpowiedź powinna być zwięzła i pomocna."
                ),
            },
            {
                "role": "user",
                "content": f"Sprawdź poniższy tekst:\n\n{user_text}",
            },
        ]
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,  
            temperature=0.7,
        )
        feedback = response.choices[0].message.content.strip()
        return feedback

    except openai.AuthenticationError:
        return "Błąd autoryzacji: sprawdź klucz API."

    except openai.OpenAIError as e:
        return f"Wystąpił błąd: {str(e)}"


def generate_grammar_quiz(translated_text):
    quiz = []
    words = translated_text.split()  # Dzielimy tekst na słowa

    # Sprawdzamy, czy lista 'words' nie jest pusta
    if words:
        for _ in range(3):  # Generujemy 3 pytania
            random_word = random.choice(words)
            quiz.append(f"Jaką rolę gramatyczną pełni słowo '{random_word}' w tym zdaniu?")
    else:
        quiz.append("Brak słów w przetłumaczonym tekście, nie można wygenerować quizu.")

    return quiz

def generate_random_words(dest_lang, num_words=3):
    try:
        prompt = (
            f"Wygeneruj {num_words} losowych słów w języku {dest_lang} wraz z ich tłumaczeniem na język polski. "
            f"Podaj je w formacie:\n1. słowo (tłumaczenie)\n2. ..."
        )
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.9
        )
        result_text = response.choices[0].message.content.strip()

        words = []
        for line in result_text.split("\n"):
            parts = line.strip().split(". ", 1)
            if len(parts) == 2 and "(" in parts[1] and ")" in parts[1]:
                word = parts[1].split(" (")[0].strip()
                translation = parts[1].split(" (")[1].strip(")")
                words.append((word, translation))
        return words
    except Exception as e:
        print(f"Błąd OpenAI: {e}")
        return []

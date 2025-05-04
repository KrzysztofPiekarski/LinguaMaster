# LinguaMaster - Language Learning App in Streamlit

LinguaMaster is an application for translating texts, storing vocabulary for memorization, processing translation history, and offering interactive language exercises. The app uses OpenAI, Langfuse, and SQLite as the database. It is being developed with users in mind who want to improve their language skills.

## Features

1. **Text Translation**
   - Translate text from one language to another using OpenAI API.
   - Supports multiple languages, including English and Polish.
   - Option to listen to the translated text using text-to-speech.

2. **Translation History**
   - View the history of previous translations.
   - Store translations in a SQLite database.
   - Option to adjust the number of translations displayed.

3. **Vocabulary to Memorize**
   - Users can add vocabulary and its translation to the database.
   - Option to view, delete, and search for vocabulary in the database.
   - Supports various languages and translations.

4. **Interactive Language Exercises**
   - The app allows users to engage in interactive language exercises to help with learning words and phrases.

## Technologies

- **Streamlit** - Platform for creating web applications in Python.
- **OpenAI GPT-4** - Used for text translation and generating responses.
- **SQLite** - Database for storing vocabulary and translation history.
- **Langfuse** - Integration for tracking interactions and data analysis.

## Installation

### Requirements

- Python 3.8+
- pip

### Step 1: Clone the repository

```bash
git clone https://github.com/YourRepository/LinguaMaster.git
cd LinguaMaster


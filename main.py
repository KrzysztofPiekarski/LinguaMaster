
import streamlit as st
import os
import boto3
from data.database import DatabaseManager  # Importujemy DatabaseManager
from ui.sidebar import sidebar_content  # Zaktualizowane wywołanie funkcji sidebar_content 

# Upewnij się, że tabele są utworzone przy uruchomieniu aplikacji
st.session_state.db.create_tables()

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
sidebar_content()  # Zaktualizowane wywołanie funkcji sidebar_content()

# ui/sidebar.py
import streamlit as st
from core.utils import get_lang_mappings

def sidebar_content():
    """Generuje zawartość bocznego panelu Streamlit z niestandardowym stylem"""

    # Stylowany tytuł sidebaru
    st.sidebar.markdown(
        """
        <div style='
            font-size: 34px;
            font-weight: 700;
            color: #4F8BF9;
            margin-bottom: 0px;
        '>📋 Szybkie Menu</div>
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
        ["Historia tłumaczeń", "Słówka", "Wyszukaj słówka"],
        key="menu_radio"
    )

    # Pobieranie mapowań języków
    lang_mapping, lang_mapping2, lang_mapping3 = get_lang_mappings()

    if menu == "Historia tłumaczeń":
        display_translation_history(lang_mapping)
    elif menu == "Słówka":
        display_vocabulary()
    elif menu == "Wyszukaj słówka":
        search_vocabulary()

def display_translation_history(lang_mapping, limit=None):
    """Wyświetla historię tłumaczeń z możliwością zmiany limitu"""
    db = st.session_state.db
    
    # Dodajemy suwak do zmiany limitu wyświetlanych tłumaczeń
    if limit is None:
        limit = st.sidebar.slider("Liczba tłumaczeń do wyświetlenia", min_value=1, max_value=50, value=5)

    history = db.get_translation_history(limit=limit)
    
    if history:
        for entry in history:
            st.sidebar.write(f"{entry[1]} → {entry[2]} ({entry[3]} → {entry[4]})")
    else:
        st.sidebar.info("Brak historii tłumaczeń.")

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

# core/utils.py
def get_lang_mappings():
    """
    Zwraca trzy mapowania języków w formie słowników, z dużą liczbą języków.
    """
    # Mapowanie dla wyświetlania w UI z flagami (np. w bocznym panelu)
    lang_mapping = {
        "Polski 🇵🇱": "pl",
        "Angielski 🇬🇧": "en",
        "Francuski 🇫🇷": "fr",
        "Niemiecki 🇩🇪": "de",
        "Hiszpański 🇪🇸": "es",
        "Włoski 🇮🇹": "it",
        "Rosyjski 🇷🇺": "ru",
        "Portugalski 🇵🇹": "pt",
        "Chiński 🇨🇳": "zh",
        "Japoński 🇯🇵": "ja",
        "Koreański 🇰🇷": "ko",
        "Holenderski 🇳🇱": "nl",
        "Szwedzki 🇸🇪": "sv",
        "Norweski 🇳🇴": "no",
        "Duński 🇩🇰": "da",
        "Fiński 🇫🇮": "fi",
        "Turecki 🇹🇷": "tr",
        "Czeski 🇨🇿": "cs",
        "Grecki 🇬🇷": "el",
        "Arabski 🇸🇦": "ar",
        "Hebrajski 🇮🇱": "he",
        "Hindi 🇮🇳": "hi",
        "Bengalski 🇧🇩": "bn",
        "Tajski 🇹🇭": "th",
        "Wietnamski 🇻🇳": "vi"
    }

    # Mapowanie w drugą stronę (z języka na flagę)
    lang_mapping2 = {value: key for key, value in lang_mapping.items()}

    # Mapa dla ogólnych tłumaczeń (np. do translacji tekstu)
    lang_mapping3 = {
        "pl": "Polski 🇵🇱",
        "en": "Angielski 🇬🇧",
        "fr": "Francuski 🇫🇷",
        "de": "Niemiecki 🇩🇪",
        "es": "Hiszpański 🇪🇸",
        "it": "Włoski 🇮🇹",
        "ru": "Rosyjski 🇷🇺",
        "pt": "Portugalski 🇵🇹",
        "zh": "Chiński 🇨🇳",
        "ja": "Japoński 🇯🇵",
        "ko": "Koreański 🇰🇷",
        "nl": "Holenderski 🇳🇱",
        "sv": "Szwedzki 🇸🇪",
        "no": "Norweski 🇳🇴",
        "da": "Duński 🇩🇰",
        "fi": "Fiński 🇫🇮",
        "tr": "Turecki 🇹🇷",
        "cs": "Czeski 🇨🇿",
        "el": "Grecki 🇬🇷",
        "ar": "Arabski 🇸🇦",
        "he": "Hebrajski 🇮🇱",
        "hi": "Hindi 🇮🇳",
        "bn": "Bengalski 🇧🇩",
        "th": "Tajski 🇹🇭",
        "vi": "Wietnamski 🇻🇳"
    }

    return lang_mapping, lang_mapping2, lang_mapping3
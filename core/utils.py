# core/utils.py
def get_lang_mappings():
    """
    Zwraca trzy mapowania języków w formie słowników, z dużą liczbą języków.
    """
    # Mapowanie dla wyświetlania w UI z flagami (np. w bocznym panelu)
    lang_mapping = {
        "Polski (pl) 🇵🇱": "Polski 🇵🇱",
        "Angielski (en) 🇬🇧": "Angielski 🇬🇧",
        "Francuski (fr) 🇫🇷": "Francuski 🇫🇷",
        "Niemiecki (de) 🇩🇪": "Niemiecki 🇩🇪",
        "Hiszpański (es) 🇪🇸": "Hiszpański 🇪🇸",
        "Włoski (it) 🇮🇹": "Włoski 🇮🇹",
        "Rosyjski (ru) 🇷🇺": "Rosyjski 🇷🇺",
        "Portugalski (pt) 🇵🇹": "Portugalski 🇵🇹",
        "Chiński (zh) 🇨🇳": "Chiński 🇨🇳",
        "Japoński (ja) 🇯🇵": "Japoński 🇯🇵",
        "Koreański (ko) 🇰🇷": "Koreański 🇰🇷",
        "Holenderski (nl) 🇳🇱": "Holenderski 🇳🇱",
        "Szwedzki (sv) 🇸🇪": "Szwedzki 🇸🇪",
        "Norweski (no) 🇳🇴": "Norweski 🇳🇴",
        "Duński (da) 🇩🇰": "Duński 🇩🇰",
        "Fiński (fi) 🇫🇮": "Fiński 🇫🇮",
        "Turecki (tr) 🇹🇷": "Turecki 🇹🇷",
        "Czeski (cs) 🇨🇿": "Czeski 🇨🇿",
        "Grecki (el) 🇬🇷": "Grecki 🇬🇷",
        "Arabski (ar) 🇸🇦": "Arabski 🇸🇦",
        "Hebrajski (he) 🇮🇱": "Hebrajski 🇮🇱",
        "Hindi (hi) 🇮🇳": "Hindi 🇮🇳",
        "Bengalski (bn) 🇧🇩": "Bengalski 🇧🇩",
        "Tajski (th) 🇹🇭": "Tajski 🇹🇭",
        "Wietnamski (vi) 🇻🇳": "Wietnamski 🇻🇳"
    }

    # Mapowanie w drugą stronę (z języka na flagę)
    lang_mapping2 = {value: key for key, value in lang_mapping.items()}

    # Mapa dla ogólnych tłumaczeń (np. do translacji tekstu)
    lang_mapping3 = {
       "Polski (pl) 🇵🇱": "Polski 🇵🇱",
        "Angielski (en) 🇬🇧": "Angielski 🇬🇧",
        "Francuski (fr) 🇫🇷": "Francuski 🇫🇷",
        "Niemiecki (de) 🇩🇪": "Niemiecki 🇩🇪",
        "Hiszpański (es) 🇪🇸": "Hiszpański 🇪🇸",
        "Włoski (it) 🇮🇹": "Włoski 🇮🇹",
        "Rosyjski (ru) 🇷🇺": "Rosyjski 🇷🇺",
        "Portugalski (pt) 🇵🇹": "Portugalski 🇵🇹",
        "Chiński (zh) 🇨🇳": "Chiński 🇨🇳",
        "Japoński (ja) 🇯🇵": "Japoński 🇯🇵",
        "Koreański (ko) 🇰🇷": "Koreański 🇰🇷",
        "Holenderski (nl) 🇳🇱": "Holenderski 🇳🇱",
        "Szwedzki (sv) 🇸🇪": "Szwedzki 🇸🇪",
        "Norweski (no) 🇳🇴": "Norweski 🇳🇴",
        "Duński (da) 🇩🇰": "Duński 🇩🇰",
        "Fiński (fi) 🇫🇮": "Fiński 🇫🇮",
        "Turecki (tr) 🇹🇷": "Turecki 🇹🇷",
        "Czeski (cs) 🇨🇿": "Czeski 🇨🇿",
        "Grecki (el) 🇬🇷": "Grecki 🇬🇷",
        "Arabski (ar) 🇸🇦": "Arabski 🇸🇦",
        "Hebrajski (he) 🇮🇱": "Hebrajski 🇮🇱",
        "Hindi (hi) 🇮🇳": "Hindi 🇮🇳",
        "Bengalski (bn) 🇧🇩": "Bengalski 🇧🇩",
        "Tajski (th) 🇹🇭": "Tajski 🇹🇭",
        "Wietnamski (vi) 🇻🇳": "Wietnamski 🇻🇳"
    }

    return lang_mapping, lang_mapping2, lang_mapping3
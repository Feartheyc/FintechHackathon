from translate import Translator

LANG_CODE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Marathi": "mr",
    "Telugu": "te",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Odia": "or",
    "Punjabi": "pa",
    "Assamese": "as",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Urdu": "ur",
    "Nepali": "ne",
    "Sanskrit": "sa"
}

def Translating(text, lang="English"):
    if lang not in LANG_CODE_MAP:
        print(f"Warning: '{lang}' not found in LANG_CODE_MAP, returning original text")
        return text
    lang_code = LANG_CODE_MAP[lang]
    translator = Translator(to_lang=lang_code)
    try:
        return translator.translate(text)
    except Exception as e:
        print(f"Translation failed for '{text}' to '{lang_code}':", e)
        return text

# translation.py
from translate import Translator

# Map Streamlit language codes to ISO language codes (translate library uses ISO codes)
LANG_CODE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    # Add more as needed
}

def translate_text(text, lang="English"):
    """Translate a string to the chosen language using offline/free method."""
    lang_code = LANG_CODE_MAP.get(lang, "en")
    translator = Translator(to_lang=lang_code)
    try:
        return translator.translate(text)
    except Exception as e:
        print(f"Translation failed for '{text}' to '{lang_code}':", e)
        return text  # fallback to original text

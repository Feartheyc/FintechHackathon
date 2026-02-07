import streamlit as st
import base64
import streamlit.components.v1 as components
import re
from content import GLOSSARY 
from translate import Translator

# --- 1. TRANSLATION ENGINE ---

LANG_CODE_MAP = {
    "English": "en", "Hindi": "hi", "Bengali": "bn", "Marathi": "mr",
    "Telugu": "te", "Tamil": "ta", "Gujarati": "gu", "Odia": "or",
    "Gujarati": "gu", "Punjabi": "pa", "Kannada": "kn", "Malayalam": "ml"
}

@st.cache_data
def translate_text(text, target_lang="English"):
    if target_lang == "English" or not text:
        return text
    
    lang_code = LANG_CODE_MAP.get(target_lang, "en")
    try:
        translator = Translator(to_lang=lang_code)
        return translator.translate(text)
    except Exception as e:
        return text

def t(text):
    """Helper function to translate strings based on session state."""
    selected_lang = st.session_state.get("selected_lang", "English")
    return translate_text(text, selected_lang)

def render_language_selector():
    """Renders a sticky-style language selector at the top of the page."""
    if "selected_lang" not in st.session_state:
        st.session_state.selected_lang = "English"

    # Floating-style container at the top
    cols = st.columns([5, 1.2])
    with cols[1]:
        lang = st.selectbox(
            "Language",
            options=list(LANG_CODE_MAP.keys()),
            index=list(LANG_CODE_MAP.keys()).index(st.session_state.selected_lang),
            label_visibility="collapsed",
            key="global_lang_selector"
        )
        if lang != st.session_state.selected_lang:
            st.session_state.selected_lang = lang
            st.rerun()
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# --- 2. EXISTING UTILS (UPDATED) ---

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return "" 

def play_narration(text):
    if text:
        # Translate narration before speaking
        translated_text = t(text)
        clean_text = translated_text.replace("'", "\\'").replace("\n", " ")
        
        # Detection for Hindi TTS vs English TTS
        is_hindi = any("\u0900" <= char <= "\u097F" for char in translated_text)
        lang_code = "hi-IN" if is_hindi else "en-GB"
        
        components.html(
            f"""
            <script>
                window.parent.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{clean_text}');
                msg.lang = '{lang_code}';
                msg.rate = 0.9;
                window.parent.speechSynthesis.speak(msg);
            </script>
            """,
            height=0,
        )

def render_interactive_dialogue(avatar, npc, text):
    # 1. Translate the main dialogue text
    translated_main_text = t(text)
    processed_text = translated_main_text
    
    # 2. Handle Glossary (Definitions also get translated)
    sorted_keys = sorted(GLOSSARY.keys(), key=len, reverse=True)
    for term in sorted_keys:
        pattern = re.compile(f"\\b({re.escape(term)})\\b", re.IGNORECASE)
        if pattern.search(processed_text):
            # Translate the definition inside the tooltip
            translated_def = t(GLOSSARY[term]).replace("'", "&apos;").replace('"', '&quot;')
            translated_term = t(term)
            
            replacement = f"<span class='highlight' onclick=\"showDef('{translated_term}', '{translated_def}')\">\\1</span>"
            processed_text = pattern.sub(replacement, processed_text)

    html_content = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Poppins', sans-serif; background-color: transparent; color: #e2e8f0; margin: 0; padding: 10px; overflow: hidden; }}
            .dialogue-container {{ display: flex; gap: 15px; align-items: flex-start; }}
            .avatar-box {{ width: 50px; height: 50px; background: #334155; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; border: 2px solid #475569; flex-shrink: 0; }}
            .speech-bubble {{ background: #1e293b; border: 1px solid #475569; padding: 15px 20px; border-radius: 0 15px 15px 15px; color: #e2e8f0; flex-grow: 1; font-size: 16px; position: relative; }}
            .speaker-name {{ color: #facc15; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; display: block; }}
            .highlight {{ color: #facc15; text-decoration: underline; text-decoration-style: dotted; cursor: help; font-weight: 600; }}
            #modal {{ display: none; position: fixed; bottom: 5px; left: 5px; right: 5px; background: #0f172a; border: 1px solid #facc15; border-left: 5px solid #facc15; padding: 12px; border-radius: 8px; z-index: 100; }}
            .modal-header {{ display: flex; justify-content: space-between; align-items: center; }}
            .modal-title {{ color: #facc15; font-weight: bold; font-size: 0.85em; }}
            .modal-close {{ cursor: pointer; color: #94a3b8; font-size: 1.2em; }}
        </style>
    </head>
    <body>
        <div class="dialogue-container">
            <div class="avatar-box">{avatar}</div>
            <div class="speech-bubble">
                <span class="speaker-name">{t(npc)}</span>
                {processed_text}
            </div>
        </div>
        <div id="modal">
            <div class="modal-header">
                <div><span class="speak-btn" onclick="speakText()">🔊</span><span id="modal-title" class="modal-title">TERM</span></div>
                <span class="modal-close" onclick="closeModal()">×</span>
            </div>
            <div id="modal-text" style="color: #cbd5e1; font-size: 0.9em; margin-top: 5px;">Def</div>
        </div>
        <script>
            function showDef(term, def) {{
                document.getElementById('modal-title').innerText = term;
                document.getElementById('modal-text').innerText = def;
                document.getElementById('modal').style.display = 'block';
            }}
            function closeModal() {{ document.getElementById('modal').style.display = 'none'; window.parent.speechSynthesis.cancel(); }}
            function speakText() {{
                window.parent.speechSynthesis.cancel();
                var text = document.getElementById('modal-text').innerText;
                var msg = new SpeechSynthesisUtterance(text);
                msg.lang = '{ "hi-IN" if st.session_state.selected_lang == "Hindi" else "en-GB" }';
                window.parent.speechSynthesis.speak(msg);
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_content, height=200)
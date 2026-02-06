import streamlit as st
import base64
import streamlit.components.v1 as components

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return "" 

def play_narration(text):
    """Additive feature: Detects language and uses the native browser Web Speech API."""
    if text:
        clean_text = text.replace("'", "\\'").replace("\n", " ")
        is_hindi = any("\u0900" <= char <= "\u097F" for char in text)
        lang_code = "hi-IN" if is_hindi else "en-GB"
        components.html(
            f"""
            <script>
                window.parent.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{clean_text}');
                msg.lang = '{lang_code}';
                msg.rate = 0.9;
                var voices = window.parent.speechSynthesis.getVoices();
                for(var i = 0; i < voices.length; i++) {{
                    if(voices[i].lang.indexOf('{lang_code}') !== -1) {{
                        msg.voice = voices[i];
                        break;
                    }}
                }}
                window.parent.speechSynthesis.speak(msg);
            </script>
            """,
            height=0,
        )
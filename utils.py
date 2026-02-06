import streamlit as st
import base64
import streamlit.components.v1 as components
import re
from content import GLOSSARY 

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return "" 

def play_narration(text):
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
                window.parent.speechSynthesis.speak(msg);
            </script>
            """,
            height=0,
        )

# --- UPDATED: Renders the WHOLE bubble (Avatar + Text) in one block ---
def render_interactive_dialogue(avatar, npc, text):
    processed_text = text
    # Sort keys by length
    sorted_keys = sorted(GLOSSARY.keys(), key=len, reverse=True)
    
    for term in sorted_keys:
        pattern = re.compile(f"\\b({re.escape(term)})\\b", re.IGNORECASE)
        if pattern.search(processed_text):
            definition = GLOSSARY[term].replace("'", "&apos;").replace('"', '&quot;')
            # Wrap in span with onclick event
            replacement = f"<span class='highlight' onclick=\"showDef('{term}', '{definition}')\">\\1</span>"
            processed_text = pattern.sub(replacement, processed_text)

    html_content = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Poppins', sans-serif; background-color: transparent; color: #e2e8f0; margin: 0; padding: 10px; overflow: hidden; }}
            
            /* FLEX CONTAINER FOR AVATAR + BUBBLE */
            .dialogue-container {{ display: flex; gap: 15px; align-items: flex-start; }}
            
            .avatar-box {{ 
                width: 50px; height: 50px; background: #334155; border-radius: 50%; 
                display: flex; align-items: center; justify-content: center; 
                font-size: 28px; border: 2px solid #475569; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.3); flex-shrink: 0; 
            }}
            
            .speech-bubble {{ 
                background: #1e293b; border: 1px solid #475569; padding: 15px 20px; 
                border-radius: 0 15px 15px 15px; color: #e2e8f0; position: relative; flex-grow: 1; 
                font-size: 16px; line-height: 1.5; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            
            .speaker-name {{ 
                color: #facc15; font-size: 0.75rem; font-weight: 800; 
                text-transform: uppercase; margin-bottom: 5px; display: block; letter-spacing: 1px;
            }}
            
            .highlight {{ 
                color: #facc15; text-decoration: underline; text-decoration-style: dotted; 
                cursor: help; font-weight: 600; transition: all 0.2s;
            }}
            .highlight:hover {{ color: #fbbf24; background: rgba(250, 204, 21, 0.2); border-radius: 4px; }}

            /* MODAL STYLING */
            #modal {{ 
                display: none; position: fixed; bottom: 5px; left: 5px; right: 5px; 
                background: #0f172a; border: 1px solid #facc15; border-left: 5px solid #facc15; 
                padding: 12px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.9); 
                z-index: 100; font-size: 0.9em;
            }}
            
            .modal-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }}
            .modal-title {{ color: #facc15; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }}
            .modal-close {{ cursor: pointer; color: #94a3b8; font-size: 1.2em; }}
            .speak-btn {{ cursor: pointer; margin-right: 8px; font-size: 1.1em; }}
        </style>
    </head>
    <body>
        <div class="dialogue-container">
            <div class="avatar-box">{avatar}</div>
            <div class="speech-bubble">
                <span class="speaker-name">{npc}</span>
                {processed_text}
            </div>
        </div>

        <div id="modal">
            <div class="modal-header">
                <div>
                    <span class="speak-btn" onclick="speakText()">🔊</span>
                    <span id="modal-title" class="modal-title">TERM</span>
                </div>
                <span class="modal-close" onclick="closeModal()">×</span>
            </div>
            <div id="modal-text" style="color: #cbd5e1;">Definition goes here.</div>
        </div>

        <script>
            function showDef(term, def) {{
                document.getElementById('modal-title').innerText = term;
                document.getElementById('modal-text').innerText = def;
                document.getElementById('modal').style.display = 'block';
            }}
            function closeModal() {{
                document.getElementById('modal').style.display = 'none';
                window.parent.speechSynthesis.cancel();
            }}
            function speakText() {{
                window.parent.speechSynthesis.cancel();
                var text = document.getElementById('modal-text').innerText;
                var msg = new SpeechSynthesisUtterance(text);
                window.parent.speechSynthesis.speak(msg);
            }}
        </script>
    </body>
    </html>
    """
    # Increased height to fit bubble + popup if needed
    components.html(html_content, height=200, scrolling=False)
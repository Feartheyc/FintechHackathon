import streamlit as st
import streamlit.components.v1 as components
from sidebar import render_sidebar
from utils import (
    img_to_base64, 
    play_narration, 
    render_interactive_dialogue, 
    render_language_selector, 
    t
)
from engine import init_game, try_apply_effects
from content import get_event_data, STATIC_CAMPAIGNS, STUDENT_EVENTS
from config import apply_custom_css
from leaderboard import render_leaderboard_ui
from phishing_game import render_phishing_game

# ==========================================
# 1. APP CONFIGURATION & STATE INITIALIZATION
# ==========================================
st.set_page_config(page_title="Financial Journey", layout="wide", page_icon="🌏", initial_sidebar_state="collapsed")

# Initialize Language State (CRITICAL for utils.py)
if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = "English"

# Initialize Game State
if "game" not in st.session_state: 
    st.session_state.game = {"state": "MAIN_MENU"}

MAP_IMG = img_to_base64("assets/level_map.png")
apply_custom_css()

# ==========================================
# 2. MENU RENDERING FUNCTIONS
# ==========================================
def render_main_menu():
    st.markdown(f'<div class="menu-title">🌏 {t("FinLife")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="menu-subtitle">{t("A Financial Literacy RPG Journey")}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"🚀 {t('START JOURNEY')}"):
            st.session_state.game['state'] = "INTRO"
            st.rerun()
        
        st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
        
        if st.button(f"📜 {t('HOW TO PLAY')}"):
            st.session_state.game['state'] = "TUTORIAL"
            st.rerun()
            
        st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)

        if st.button(f"🛡️ {t('CYBER SHIELD TRAINING')}"):
            st.session_state.game['state'] = "CYBER_GAME"
            st.rerun()

        st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)

        if st.button(f"❤️ {t('CREDITS')}"):
            st.session_state.game['state'] = "CREDITS"
            st.rerun()

def render_credits():
    st.markdown(f'<div class="menu-title" style="font-size: 3rem;">{t("CREDITS")}</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class="menu-card">
                <h2 style="color:#4ade80;">{t("Developed Team FinLife")}</h2>
                <p style="color:#94a3b8;">{t("Created for the FinTech Hackathon 2026")}</p>
                <hr style="border-color: #334155;">
                <p style="text-align:left;">
                <b>• {t("Team")}:</b> Yashvi Parikh, Yuvraj Chavan, Devansh Bakrania<br>
                <b>• {t("Tech Stack")}:</b> Python, Streamlit, Pandas, SQLite<br>
                <b>• {t("Features")}:</b> {t("RPG Gameplay, Stock Simulator, Cyber Safety")}<br>
                <b>• {t("Mission")}:</b> {t("Making financial literacy accessible to rural India.")}
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"⬅ {t('BACK TO MENU')}"):
            st.session_state.game['state'] = "MAIN_MENU"
            st.rerun()

def render_tutorial():
    st.markdown(f'<div class="menu-title" style="font-size: 3rem;">{t("HOW TO PLAY")}</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class="menu-card" style="text-align: left;">
                <h3 style="color:#facc15;">1. {t("Choose Your Persona")}</h3>
                <p>{t("Select from Farmer, Student, Employee, or Founder. Each has unique financial challenges.")}</p>
                <h3 style="color:#facc15;">2. {t("Make Smart Choices")}</h3>
                <p>{t("Navigate real-life scenarios. Every decision affects your Cash, Savings, and Stress.")}</p>
                <h3 style="color:#facc15;">3. {t("Use Your Tools")}</h3>
                <p>{t("Check the Stock Market Simulator to grow wealth or the Cyber Shield to learn security.")}</p>
                <h3 style="color:#facc15;">4. {t("Win the Game")}</h3>
                <p>{t("Survive the debt traps and build the highest Net Worth to win!")}</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"⬅ {t('BACK TO MENU')}"):
            st.session_state.game['state'] = "MAIN_MENU"
            st.rerun()

# ==========================================
# 3. HELPERS
# ==========================================
def format_effects(effects):
    changes = []
    for k in ["cash", "savings", "loan", "investments"]:
        if k in effects and effects[k] != 0:
            val, sign = effects[k], "+" if effects[k] > 0 else "-"
            # TranslateTranslate the keys for the labels
            changes.append(f"{sign}₹{abs(val):,} {t(k.capitalize())}")
    return f" ({', '.join(changes)})" if changes else ""

def render_hud_content(p):
    ins_status = f"✅ {t('Active')}" if p['insurance'] else f"❌ {t('None')}"
    return f"""
    <div class="hud-container">
        <div class="hud-item"><div class="hud-label">{t("ROLE")}</div><div class="hud-value">{t(p['persona'])}</div></div>
        <div class="hud-item"><div class="hud-label">{t("CASH")}</div><div class="hud-value money-val">₹{p['cash']:,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("SAVINGS")}</div><div class="hud-value money-val">₹{p['savings']:,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("DEBT")}</div><div class="hud-value debt-val">₹{p['loan']:,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("INVEST")}</div><div class="hud-value invest-val">₹{p['investments']:,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("STRESS")}</div><div class="hud-value stress-val">{p['stress']}%</div></div>
        <div class="hud-item"><div class="hud-label">{t("INSURANCE")}</div><div class="hud-value ins-val">{ins_status}</div></div>
    </div>
    """

def render_mini_map(persona, current_lvl):
    if persona == "Student":
        total_levels = len(STUDENT_EVENTS)
    else:
        total_levels = len(STATIC_CAMPAIGNS.get(persona, {}))
    
    dots_html = ""
    for i in range(total_levels):
        if i < current_lvl:
            status = "completed"
            content = "✓"
        elif i == current_lvl:
            status = "active"
            content = ""
        else:
            status = "pending"
            content = ""
            
        dots_html += f"<div class='step {status}'>{content}</div>"
        
        if i < total_levels - 1:
            line_status = "line-active" if i < current_lvl else "line-pending"
            dots_html += f"<div class='step-line {line_status}'></div>"

    return f"""
<style>
    .progress-wrapper {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 15px 20px;
        margin-bottom: 20px;
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}
    .step {{
        width: 24px; height: 24px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 12px;
        z-index: 2;
        transition: all 0.3s;
    }}
    .step.completed {{ background: #4ade80; color: #064e3b; box-shadow: 0 0 8px rgba(74, 222, 128, 0.4); }}
    .step.active {{ 
        background: #ff5252; border: 2px solid white; 
        box-shadow: 0 0 12px rgba(255, 82, 82, 0.8); 
        transform: scale(1.3);
    }}
    .step.pending {{ background: #334155; border: 2px solid #475569; }}
    
    .step-line {{
        flex-grow: 1;
        height: 4px;
        margin: 0 2px;
        border-radius: 2px;
    }}
    .line-active {{ background: #4ade80; }}
    .line-pending {{ background: #334155; }}
</style>
<div class="progress-wrapper">
    {dots_html}
</div>
"""

# ==========================================
# 4. SCENE RENDERING
# ==========================================
def render_persona_selection():
    st.markdown(f"<h1 style='text-align:center; font-size: 3rem;'>🌏 {t('FinLife')}</h1>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    chars = [
        {"col": c1, "role": "Farmer", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825021.png", "desc": "Crops and weather risks.", "btn": "🚜 Select Farmer"},
        {"col": c2, "role": "Employee", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825038.png", "desc": "Salary and office politics.", "btn": "👔 Select Employee"},
        {"col": c3, "role": "Student", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825108.png", "desc": "Pocket money and choices.", "btn": "🎓 Select Student"},
        {"col": c4, "role": "Founder", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825072.png", "desc": "High risk, chasing unicorns.", "btn": "🚀 Select Founder"}
    ]
    for char in chars:
        with char["col"]:
            st.markdown(f'<div class="char-card"><img src="{char["img"]}" class="char-img"><h3>{t(char["role"])}</h3><p>{char["desc"]}</p></div>', unsafe_allow_html=True)
            if st.button(char["btn"], key=f"sel_{char['role']}", use_container_width=True):
                st.session_state.game = init_game(char["role"])
                st.rerun()
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button(f"⬅ {t('Back to Main Menu')}", use_container_width=True):
        st.session_state.game['state'] = "MAIN_MENU"
        st.rerun()

def render_map():
    p = st.session_state.game
    current_lvl = p['event_index']
    st.markdown(render_hud_content(p), unsafe_allow_html=True)
    
    c1, c2 = st.columns([3, 1])
    with c1:
        persona_map_files = {"Farmer": "assets/map_farmer.png", "Student": "assets/map_student.png", "Employee": "assets/map_business.png", "Founder": "assets/map_startup.png"}
        target_map_file = persona_map_files.get(p['persona'], "assets/level_map.png")
        current_map_img = img_to_base64(target_map_file) or img_to_base64("assets/level_map.png")

        path = [(10, 80), (20, 70), (30, 75), (40, 60), (50, 50), (60, 45), (70, 55), (80, 40), (90, 30)]
        svg = f'<polyline points="{" ".join([f"{x*8},{y*6}" for x,y in path])}" fill="none" stroke="#ffd966" stroke-width="6" stroke-dasharray="10,5"/>'
        for idx, (bx, by) in enumerate(path):
            color = "#4ade80" if idx < current_lvl else ("#ff5252" if idx == current_lvl else "#64748b")
            svg += f'<circle cx="{bx*8}" cy="{by*6}" r="{15 if idx==current_lvl else 10}" fill="{color}" stroke="white" stroke-width="2"><animate attributeName="r" values="15;18;15" dur="1.5s" repeatCount="indefinite" /></circle>' if idx == current_lvl else f'<circle cx="{bx*8}" cy="{by*6}" r="10" fill="{color}" stroke="white" stroke-width="2"></circle>'
        
        components.html(f"<style>body {{ margin: 0; overflow: hidden; }} #map-container {{ width: 100%; height: 600px; background-image: url('data:image/png;base64,{current_map_img}'); background-size: cover; background-position: center; border-radius: 12px; }} </style><div id='map-container'><svg viewBox='0 0 800 600' preserveAspectRatio='none'>{svg}</svg></div>", height=620)
            
    with c2:
        st.markdown(f"### {t('Level')} {current_lvl + 1}")
        evt = get_event_data(p['persona'], current_lvl)
        if evt:
            if st.button(f"🚀 {t('Enter Level')}", type="primary", use_container_width=True): 
                st.session_state.game['state'] = "PLAYING"
                st.rerun()
        else:
            if st.button(f"🏆 {t('Finish')}", type="primary"): 
                st.session_state.game['state'] = "END"
                st.rerun()
        
        st.markdown("---")
        st.markdown(f"### 🏛️ {t('NSE Terminal')}")
        if st.button(f"📈 {t('Open Stock Market')}", use_container_width=True):
            st.session_state.cash = float(p['cash'])
            st.session_state.username = p['persona']
            st.session_state.game['state'] = "MARKET"
            st.rerun()
            
        st.markdown("---")
        if st.button(f"⬅ {t('Change Role')}"): 
            st.session_state.game['state'] = "INTRO"
            st.rerun()

def render_scene():
    p = st.session_state.game
    evt = get_event_data(p['persona'], p['event_index'])
    if not evt: p['state'] = "MAP"; st.rerun(); return
    
    # Text is translated inside utils.py automatically
    play_narration(evt['story'])
    render_sidebar(p)
    
    _, c2, _ = st.columns([1, 4, 1])
    with c2:
        st.markdown(render_hud_content(p), unsafe_allow_html=True)
        st.markdown(render_mini_map(p['persona'], p['event_index']), unsafe_allow_html=True)
        st.markdown('<div class="scene-card">', unsafe_allow_html=True)
        
        if p.get('last_feedback'):
            st.markdown(f"<div class='game-alert alert-{p['feedback_type']}'>{t(p['last_feedback'])}</div>", unsafe_allow_html=True)
            p['last_feedback'] = None
        
        # UI rendering handles internal translation
        render_interactive_dialogue(evt["avatar"], evt["npc"], evt["story"])
        
        if "thought" in evt: 
            st.markdown(f'<div class="thought-container"><div class="thought-bubble">💭 {t(evt["thought"])}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if "advisor" in evt:
            with st.expander(f"💡 {t('Ask Financial Advisor')}"):
                st.markdown(f"**{t('Expert Recommendation')}:**\n\n{t(evt['advisor'])}")

        if "choices" in evt:
            cols = st.columns(len(evt["choices"]))
            for i, (txt, eff) in enumerate(evt["choices"].items()):
                with cols[i]:
                    if st.button(f"{t(txt)}{format_effects(eff)}", key=f"btn_{p['event_index']}_{i}"):
                        msg = eff.pop('__msg', None)
                        success, s_msg = try_apply_effects(eff)
                        p['last_feedback'], p['feedback_type'] = (msg or s_msg), ("good" if success else "bad")
                        if success: p['event_index'] += 1
                        st.rerun()
        elif "auto" in evt:
            if st.button(f"{t('Continue')} ➡️", type="primary"): 
                try_apply_effects(evt["auto"]); p['event_index'] += 1; st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"🗺️ {t('Map')}"): p['state'] = "MAP"; st.rerun()

# ==========================================
# 5. MAIN LOOP
# ==========================================
# Render the Dropdown at the VERY top
render_language_selector()

state = st.session_state.game['state']

if state == "MAIN_MENU":
    render_main_menu()
elif state == "CREDITS":
    render_credits()
elif state == "TUTORIAL":
    render_tutorial()
elif state == "INTRO": 
    render_persona_selection()
elif state == "CYBER_GAME": 
    render_phishing_game()
elif state == "MAP": 
    render_map()
elif state == "PLAYING": 
    render_scene()
elif state == "MARKET":
    try:
        with open("investmentsim.py", encoding="utf-8") as f:
            exec(f.read())
    except FileNotFoundError:
        st.error(t("investmentsim.py not found!"))
        if st.button(t("Back to Map")): st.session_state.game['state'] = "MAP"; st.rerun()
elif state == "END":
    p = st.session_state.game
    nw = (p['cash'] + p['savings'] + p['investments']) - p['loan']
    st.balloons()
    st.markdown(f"<div class='menu-card'><h1>{t('Journey Complete')}</h1><h2>{t('Net Worth')}: ₹{nw:,}</h2></div>", unsafe_allow_html=True)
    render_leaderboard_ui(final_score=nw)
    if st.button(f"↺ {t('Restart Journey')}", use_container_width=True): 
        st.session_state.game = {"state": "MAIN_MENU"}
        st.rerun()
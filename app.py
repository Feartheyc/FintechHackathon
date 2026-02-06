import streamlit as st
import streamlit.components.v1 as components
from sidebar import render_sidebar
from utils import img_to_base64, play_narration
from engine import init_game, try_apply_effects
from content import get_event_data

# ==========================================
# 1. APP CONFIGURATION
# ==========================================
st.set_page_config(page_title="Financial Journey", layout="wide", page_icon="🌏", initial_sidebar_state="expanded")
MAP_IMG = img_to_base64("assets/level_map.png")
if "game" not in st.session_state: st.session_state.game = {"state": "INTRO"}

# ==========================================
# 2. ULTRA-MODERN UI CSS (With Width Adjustment)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');
    
    .stApp { background: radial-gradient(circle at top, #1e1b4b 0%, #020617 100%); color: #e2e8f0; font-family: 'Poppins', sans-serif; }
    
    @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    /* --- HUD BAR UPDATED --- */
    .hud-container { 
        background: rgba(15, 23, 42, 0.6); 
        backdrop-filter: blur(12px); 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        border-radius: 16px; 
        padding: 15px 25px; /* Increased horizontal padding */
        display: flex; 
        justify-content: space-between; 
        margin-bottom: 25px; 
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); 
        flex-wrap: nowrap; /* Prevents items from jumping to next line */
        gap: 15px; 
        width: 100%; /* Ensure it uses full column width */
    }
    
    .hud-item { 
        text-align: center; 
        flex: 1; 
        min-width: 85px; /* Increased min-width to fit currency values */
        border-right: 1px solid rgba(255, 255, 255, 0.1); 
    }
    .hud-item:last-child { border-right: none; }
    
    .hud-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; font-weight: 600; }
    .hud-value { font-family: 'Space Mono', monospace; font-size: 1.0rem; font-weight: 700; color: #f8fafc; white-space: nowrap; }
    
    .money-val { color: #4ade80; } 
    .debt-val { color: #f87171; } 
    .stress-val { color: #facc15; }
    .invest-val { color: #c084fc; }

    /* --- GAME CARD --- */
    .scene-card { background: linear-gradient(145deg, #1e293b, #0f172a); border: 1px solid #334155; border-radius: 20px; padding: 30px; margin-bottom: 20px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5); animation: slideUp 0.5s ease-out; position: relative; overflow: hidden; }
    .scene-card::before { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899); }
    
    .dialogue-box { display: flex; gap: 15px; align-items: flex-start; margin-top: 10px; }
    .avatar-box { width: 60px; height: 60px; background: #334155; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; border: 2px solid #475569; box-shadow: 0 4px 6px rgba(0,0,0,0.3); flex-shrink: 0; }
    .speech-bubble { background: #1e293b; border: 1px solid #475569; padding: 15px 20px; border-radius: 0 15px 15px 15px; color: #e2e8f0; position: relative; flex-grow: 1; }
    .speaker-name { color: #facc15; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; display: block; }
    
    .thought-container { display: flex; justify-content: flex-end; margin-top: 15px; margin-bottom: 20px; padding-right: 10px; }
    .thought-bubble { background: rgba(99, 102, 241, 0.1); border: 1px dashed #6366f1; color: #a5b4fc; padding: 10px 20px; border-radius: 15px 0 15px 15px; font-style: italic; font-size: 0.9rem; max-width: 85%; text-align: right; }
    
    .stButton > button { width: 100%; background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); border: 1px solid #475569; padding: 20px !important; border-radius: 12px; color: #f1f5f9; font-size: 0.95rem; font-weight: 500; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); text-align: left; }
    .stButton > button:hover { border-color: #38bdf8; transform: translateY(-3px); background: linear-gradient(180deg, #334155 0%, #1e293b 100%); }
    
    .game-alert { padding: 15px; border-radius: 8px; margin-bottom: 15px; text-align: center; font-weight: bold; animation: slideUp 0.3s ease-out; border: 1px solid; }
    .alert-good { background: rgba(6, 78, 59, 0.8); border-color: #059669; color: #6ee7b7; }
    .alert-bad { background: rgba(127, 29, 29, 0.8); border-color: #dc2626; color: #fca5a5; }
    
    #map-container { border: 2px solid #334155; box-shadow: 0 0 20px rgba(0,0,0,0.5); }
    
    .char-card { background-color: #1e293b; border: 2px solid #334155; border-radius: 15px; padding: 20px; text-align: center; transition: transform 0.3s ease, border-color 0.3s ease; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: space-between; }
    .char-card:hover { transform: translateY(-5px); border-color: #38bdf8; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    .char-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; margin-bottom: 15px; border: 3px solid #475569; background: #0f172a; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HELPERS
# ==========================================
def format_effects(effects):
    changes = []
    for k in ["cash", "savings", "loan", "investments"]:
        if k in effects and effects[k] != 0:
            val, sign = effects[k], "+" if effects[k] > 0 else "-"
            changes.append(f"{sign}₹{abs(val):,} {k.capitalize()}")
    return f" ({', '.join(changes)})" if changes else ""

def render_hud_content(p):
    ins_status = "✅ Active" if p['insurance'] else "❌ None"
    return f"""
    <div class="hud-container">
        <div class="hud-item"><div class="hud-label">ROLE</div><div class="hud-value">{p['persona']}</div></div>
        <div class="hud-item"><div class="hud-label">CASH</div><div class="hud-value money-val">₹{p['cash']:,}</div></div>
        <div class="hud-item"><div class="hud-label">SAVINGS</div><div class="hud-value money-val">₹{p['savings']:,}</div></div>
        <div class="hud-item"><div class="hud-label">DEBT</div><div class="hud-value debt-val">₹{p['loan']:,}</div></div>
        <div class="hud-item"><div class="hud-label">INVEST</div><div class="hud-value invest-val">₹{p['investments']:,}</div></div>
        <div class="hud-item"><div class="hud-label">STRESS</div><div class="hud-value stress-val">{p['stress']}%</div></div>
        <div class="hud-item"><div class="hud-label">INSURANCE</div><div class="hud-value">{ins_status}</div></div>
    </div>
    """

# ==========================================
# 4. SCENE RENDERING
# ==========================================
def render_persona_selection():
    st.markdown("<h1 style='text-align:center; font-size: 3rem;'>🌏 Arth-Sagar</h1>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    chars = [
        {"col": c1, "role": "Farmer", "img": "https://cdn-icons-png.flaticon.com/512/4955/4955737.png", "desc": "Crops and weather risks.", "btn": "🚜 Select Farmer"},
        {"col": c2, "role": "Employee", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825038.png", "desc": "Salary and office politics.", "btn": "👔 Select Employee"},
        {"col": c3, "role": "Student", "img": "https://cdn-icons-png.flaticon.com/512/5853/5853761.png", "desc": "Pocket money and choices.", "btn": "🎓 Select Student"},
        {"col": c4, "role": "Founder", "img": "https://cdn-icons-png.flaticon.com/512/1995/1995669.png", "desc": "High risk, chasing unicorns.", "btn": "🚀 Select Founder"}
    ]
    for char in chars:
        with char["col"]:
            st.markdown(f'<div class="char-card"><img src="{char["img"]}" class="char-img"><h3>{char["role"]}</h3><p>{char["desc"]}</p></div>', unsafe_allow_html=True)
            if st.button(char["btn"], key=f"sel_{char['role']}", use_container_width=True):
                st.session_state.game = init_game(char["role"]); st.rerun()

def render_map():
    p = st.session_state.game
    current_lvl = p['event_index']
    st.markdown(render_hud_content(p), unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        path = [(10, 80), (20, 70), (30, 75), (40, 60), (50, 50), (60, 45), (70, 55), (80, 40), (90, 30)]
        svg = f'<polyline points="{" ".join([f"{x*8},{y*6}" for x,y in path])}" fill="none" stroke="#ffd966" stroke-width="6" stroke-dasharray="10,5"/>'
        for idx, (bx, by) in enumerate(path):
            color = "#4ade80" if idx < current_lvl else ("#ff5252" if idx == current_lvl else "#64748b")
            svg += f'<circle cx="{bx*8}" cy="{by*6}" r="{15 if idx==current_lvl else 10}" fill="{color}" stroke="white" stroke-width="2"><animate attributeName="r" values="15;18;15" dur="1.5s" repeatCount="indefinite" /></circle>' if idx == current_lvl else f'<circle cx="{bx*8}" cy="{by*6}" r="10" fill="{color}" stroke="white" stroke-width="2"></circle>'
        components.html(f"<style>body {{ margin: 0; }} #map-container {{ width: 100%; height: 600px; background-image: url('data:image/png;base64,{MAP_IMG}'); background-size: cover; border-radius: 12px; }}</style><div id='map-container'><svg viewBox='0 0 800 600'>{svg}</svg></div>", height=620)
    with c2:
        st.markdown(f"### Level {current_lvl + 1}")
        evt = get_event_data(p['persona'], current_lvl)
        if evt:
            if st.button("🚀 Enter Level", type="primary", use_container_width=True): st.session_state.game['state'] = "PLAYING"; st.rerun()
        else:
            if st.button("🏆 Finish", type="primary"): st.session_state.game['state'] = "END"; st.rerun()
        st.markdown("---")
        if st.button("⬅ Change Role"): st.session_state.game['state'] = "INTRO"; st.rerun()

def render_scene():
    p = st.session_state.game
    evt = get_event_data(p['persona'], p['event_index'])
    if not evt: p['state'] = "MAP"; st.rerun(); return
    play_narration(evt['story'])
    render_sidebar(p)
    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        st.markdown(render_hud_content(p), unsafe_allow_html=True)
        st.markdown('<div class="scene-card">', unsafe_allow_html=True)
        if p['last_feedback']:
            st.markdown(f"<div class='game-alert alert-{p['feedback_type']}'>{p['last_feedback']}</div>", unsafe_allow_html=True)
            p['last_feedback'] = None
        st.markdown(f'<div class="dialogue-box"><div class="avatar-box">{evt["avatar"]}</div><div class="speech-bubble"><span class="speaker-name">{evt["npc"]}</span>{evt["story"]}</div></div>', unsafe_allow_html=True)
        if "thought" in evt: st.markdown(f'<div class="thought-container"><div class="thought-bubble">💭 {evt["thought"]}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if "choices" in evt:
            cols = st.columns(len(evt["choices"]))
            for i, (txt, eff) in enumerate(evt["choices"].items()):
                with cols[i]:
                    if st.button(f"{txt}{format_effects(eff)}", key=f"btn_{p['event_index']}_{i}"):
                        msg = eff.pop('__msg', None)
                        success, s_msg = try_apply_effects(eff)
                        p['last_feedback'], p['feedback_type'] = (msg or s_msg), ("good" if success else "bad")
                        if success: p['event_index'] += 1
                        st.rerun()
        elif "auto" in evt:
            if st.button("Continue ➡️", type="primary"): try_apply_effects(evt["auto"]); p['event_index'] += 1; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗺️ Map"): p['state'] = "MAP"; st.rerun()

# ==========================================
# 5. MAIN LOOP
# ==========================================
state = st.session_state.game['state']
if state == "INTRO": render_persona_selection()
elif state == "MAP": render_map()
elif state == "PLAYING": render_scene()
elif state == "END":
    p = st.session_state.game
    nw = (p['cash'] + p['savings'] + p['investments']) - p['loan']
    st.balloons()
    st.markdown(f"<div style='text-align:center; padding:40px; background: rgba(15, 23, 42, 0.8); border-radius:20px; border: 1px solid #334155; margin-top: 50px;'><h1>Journey Complete</h1><h2>Net Worth: ₹{nw:,}</h2></div>", unsafe_allow_html=True)
    if st.button("↺ Restart"): st.session_state.game = {"state": "INTRO"}; st.rerun()
import streamlit as st
import time
from sidebar import render_sidebar

# ==========================================
# 1. APP CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Arth-Sagar: Omni Edition",
    page_icon="🌏",
    layout="wide",   # <-- Must be 'wide' for side-by-side layout
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ULTRA-MODERN UI CSS
# ==========================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

    /* --- GLOBAL THEME --- */
    .stApp {
        background: radial-gradient(circle at top, #1e1b4b 0%, #020617 100%);
        color: #e2e8f0;
        font-family: 'Poppins', sans-serif;
    }

    /* --- ANIMATIONS --- */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* --- HUD BAR --- */
    .hud-container {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 15px;
        display: flex;
        justify-content: space-between;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .hud-item {
        text-align: center;
        flex: 1;
        min-width: 60px;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hud-item:last-child { border-right: none; }
    
    .hud-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8;
        font-weight: 600;
    }
    
    .hud-value {
        font-family: 'Space Mono', monospace;
        font-size: 1.0rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .money-val { color: #4ade80; }
    .debt-val { color: #f87171; }
    .stress-val { color: #facc15; }

    /* --- GAME CARD --- */
    .scene-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        animation: slideUp 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .scene-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
    }

    /* --- DIALOGUE UI --- */
    .dialogue-box {
        display: flex;
        gap: 15px;
        align-items: flex-start;
        margin-top: 10px;
    }
    
    .avatar-box {
        width: 60px;
        height: 60px;
        background: #334155;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        border: 2px solid #475569;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        flex-shrink: 0;
    }
    
    .speech-bubble {
        background: #1e293b;
        border: 1px solid #475569;
        padding: 15px 20px;
        border-radius: 0 15px 15px 15px;
        color: #e2e8f0;
        position: relative;
        flex-grow: 1;
    }
    
    .speaker-name {
        color: #facc15;
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 5px;
        display: block;
    }

    /* --- PLAYER THOUGHTS --- */
    .thought-container {
        display: flex;
        justify-content: flex-end;
        margin-top: 15px;
        margin-bottom: 20px;
        padding-right: 10px;
    }
    
    .thought-bubble {
        background: rgba(99, 102, 241, 0.1);
        border: 1px dashed #6366f1;
        color: #a5b4fc;
        padding: 10px 20px;
        border-radius: 15px 0 15px 15px;
        font-style: italic;
        font-size: 0.9rem;
        max-width: 85%;
        text-align: right;
    }

    /* --- BUTTONS --- */
    .stButton > button {
        width: 100%;
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #475569;
        padding: 20px !important;
        border-radius: 12px;
        color: #f1f5f9;
        font-size: 0.95rem;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: left;
    }
    .stButton > button:hover {
        border-color: #38bdf8;
        transform: translateY(-3px);
        background: linear-gradient(180deg, #334155 0%, #1e293b 100%);
    }

    /* --- TOASTS --- */
    .game-alert {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        text-align: center;
        font-weight: bold;
        animation: slideUp 0.3s ease-out;
        border: 1px solid;
    }
    .alert-good { background: rgba(6, 78, 59, 0.8); border-color: #059669; color: #6ee7b7; }
    .alert-bad { background: rgba(127, 29, 29, 0.8); border-color: #dc2626; color: #fca5a5; }
    .alert-info { background: rgba(30, 58, 138, 0.8); border-color: #2563eb; color: #bfdbfe; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. ADVANCED LOGIC ENGINE
# ==========================================

def init_game(persona):
    defaults = {
        "Student": {"cash": 6000, "savings": 2000, "loan": 0, "investments": 0, "stress": 25},
        "Farmer": {"cash": 10000, "savings": 5000, "loan": 0, "investments": 500000, "stress": 10},
        "Employee": {"cash": 50000, "savings": 100000, "loan": 0, "investments": 50000, "stress": 40}
    }
    base = defaults[persona]
    return {
        "state": "PLAYING", "persona": persona, "event_index": 0,
        "cash": base['cash'], "savings": base['savings'], "loan": base['loan'],
        "investments": base['investments'], "insurance": False,
        "confidence": 50, "stress": base['stress'], "regret": 0,
        "history": [], "last_feedback": None, "feedback_type": "info", "flags": {}
    }

if "game" not in st.session_state:
    st.session_state.game = {"state": "INTRO"}

def try_apply_effects(effects):
    p = st.session_state.game
    
    # --- BANKRUPTCY PROTECTION ---
    savings_deduction = effects.get("savings", 0)
    cash_deduction = effects.get("cash", 0)

    if savings_deduction < 0 and p["savings"] + savings_deduction < 0:
        return False, "❌ Insufficient savings!"

    if cash_deduction < 0:
        amount = abs(cash_deduction)
        if p["cash"] < amount:
            remaining = amount - p["cash"]
            if p["savings"] - remaining < 0:
                return False, "❌ Insufficient capital!"

    # --- APPLY EFFECTS ---
    if effects.get("insurance") is False: p["insurance"] = False
    elif effects.get("insurance") is True: p["insurance"] = True

    for k, v in effects.items():
        if k == "cash" and v < 0:
            amount = abs(v)
            if p["cash"] >= amount:
                p["cash"] -= amount
            else:
                p["cash"] = 0
                p["savings"] -= (amount - p["cash"])
        elif k == "add_flag":
            p["flags"][v] = True
        elif k != "insurance":
            if k in p: p[k] += v

    return True, "✅ Decision Recorded"

# ==========================================
# 4. CONTENT DATABASE
# ==========================================

def c(text, effects, msg=None):
    return {"text": text, "effects": effects, "msg": msg}

STATIC_CAMPAIGNS = {
    "Farmer": {
        0: { 
            "title": "Sowing Season", "npc": "Moneylender Seth", "avatar": "👹", 
            "text": "Ramesh! Why run to the bank? Take ₹20,000 cash now. No paperwork.", 
            "thought": "Bank takes days... but Seth's interest is deadly. The rain is coming soon.",
            "choices": [
                c("Take Seth's Cash", {"cash": 20000, "loan": 20000, "add_flag": "predatory_loan"}, "Debt Trap: 50% Interest rate!"),
                c("Go to Bank (KCC)", {"cash": 20000, "loan": 20000, "confidence": 10}, "Safe Loan: 7% Interest.")
            ]
        },
        1: { 
            "title": "Seed Quality", "npc": "Shopkeeper", "avatar": "🏪", 
            "text": "I have Hybrid Seeds (₹3,000) and Local Seeds (₹1,000). Hybrid gives double yield but needs water.", 
            "thought": "My borewell is old... if the rains fail, hybrid crops will die.",
            "choices": [
                c("Buy Hybrid", {"cash": -3000, "add_flag": "hybrid_seeds"}, "High Potential."),
                c("Buy Local", {"cash": -1000}, "Low Cost.")
            ]
        },
        2: { 
            "title": "Harvest Price", "npc": "Middleman", "avatar": "⚖️", 
            "text": "Price is ₹10/kg here. Mandi is 50km away, but prices are better there.", 
            "thought": "I'm tired from the harvest. Going to Mandi means renting a truck.",
            "choices": [
                c("Sell Here", {"cash": 30000, "regret": 10}, "Quick cash."),
                c("Go to Mandi", {"cash": 45000, "stress": 5}, "Hard work pays off.")
            ]
        },
        3: { 
            "title": "Loan Repayment", "npc": "Bank Manager", "avatar": "🏦", 
            "text": "Namaste Ramesh. Your crop loan is due. Can you clear it today?", 
            "thought": "I have the cash, but what if an emergency comes up?",
            "choices": [
                c("Repay Full", {"cash": -20000, "loan": -20000, "confidence": 10}, "Debt Free."),
                c("Delay", {"stress": 10, "loan": 2000}, "Interest piling up.")
            ]
        },
        4: { 
            "title": "Daughter's School", "npc": "Wife", "avatar": "👩", 
            "text": "Lakshmi needs admission. The Private school is ₹15k, but the Govt school is free.", 
            "thought": "I want her to have the life I never had.",
            "choices": [
                c("Private School", {"cash": -15000, "success": 20}, "Better future."),
                c("Govt School", {"success": 5}, "Saved money.")
            ]
        },
        5: { 
            "title": "Tractor", "npc": "Dealer", "avatar": "🚜", 
            "text": "Why use bullocks? Buy a Tractor! I'll arrange a ₹5 Lakh loan instantly.", 
            "thought": "A tractor would make me a king in the village... but the debt?",
            "choices": [
                c("Buy Tractor", {"loan": 500000, "stress": 20}, "Status symbol."),
                c("Rent when needed", {"cash": -5000}, "Smart choice.")
            ]
        },
        6: { 
            "title": "Sister's Wedding", "npc": "Family", "avatar": "🎉", 
            "text": "The wedding must be grand! We need ₹2 Lakhs for the feast.", 
            "thought": "If I don't spend, the village will talk. If I do, I lose my land.",
            "choices": [
                c("Sell Land", {"cash": 500000, "add_flag": "sold_land", "regret": 20}, "Asset lost."),
                c("Simple Wedding", {"cash": -50000}, "Social pressure ignored.")
            ]
        },
    },
    "Employee": {
        0: { 
            "title": "Job Offer", "npc": "HR", "avatar": "👔", 
            "text": "Welcome aboard! We can structure your salary: High Cash in hand or Higher PF contribution?", 
            "thought": "Cash buys things today. PF buys freedom later.",
            "choices": [
                c("High Cash", {"cash": 50000}, "Instant gratification."),
                c("High PF", {"cash": 40000, "savings": 10000}, "Retirement secured.")
            ]
        },
        1: { 
            "title": "New Phone", "npc": "Advertisement", "avatar": "📱", 
            "text": "Flash Sale! The iPhone 16 Pro Max is finally here. EMI starts at ₹5000!", 
            "thought": "My current phone works fine, but everyone at the office has the new one...",
            "choices": [
                c("Buy on EMI", {"loan": 80000, "regret": 10}, "Costly status."),
                c("Keep Old Phone", {"savings": 5000}, "Saved money.")
            ]
        },
        2: { 
            "title": "Car Purchase", "npc": "Family", "avatar": "🚗", 
            "text": "Everyone else has a new car. We should get an SUV!", 
            "thought": "An SUV is a status symbol, but a hatchback is debt-free.",
            "choices": [
                c("New SUV", {"loan": 1500000, "stress": 10}, "Big EMI."),
                c("Used Hatchback", {"cash": -200000}, "Debt free.")
            ]
        },
        3: { 
            "title": "Stock Tip", "npc": "Friend", "avatar": "📉", 
            "text": "Bro, I heard this penny stock is going to double in 2 days. Invest now!", 
            "thought": "Get rich quick schemes usually end badly... but what if he's right?",
            "choices": [
                c("Gamble", {"cash": -50000, "regret": 20}, "Lost everything."),
                c("Stick to SIP", {"investments": 20000}, "Disciplined.")
            ]
        },
        4: { 
            "title": "Medical Insurance", "npc": "Insurance Agent", "avatar": "🏥", 
            "text": "Sir, one medical emergency can wipe your savings. Cover parents for just ₹25k?", 
            "thought": "I'm young and healthy. Do I really need this expense?",
            "choices": [
                c("Buy Policy", {"cash": -25000, "insurance": True}, "Safety net."),
                c("Skip", {}, "Huge risk.")
            ]
        },
        5: { 
            "title": "Home Renovation", "npc": "Contractor", "avatar": "🔨", 
            "text": "The kitchen looks old. Let's redo it completely for ₹3 Lakhs.", 
            "thought": "It would look great, but I'd have to take a personal loan.",
            "choices": [
                c("Personal Loan", {"loan": 300000}, "High interest."),
                c("Delay", {"stress": 5}, "Save first.")
            ]
        },
        6: { 
            "title": "Layoff Rumors", "npc": "Colleague", "avatar": "🏢", 
            "text": "Did you hear? They might fire 20% of the staff next month.", 
            "thought": "Panic won't help. I should probably save cash and upskill.",
            "choices": [
                c("Up-skill Course", {"cash": -5000, "confidence": 10}, "Safe."),
                c("Ignore", {"stress": 20}, "Risky.")
            ]
        },
    }
}

# --- DYNAMIC PYTHON LOGIC CONTENT (STUDENT) ---
def stud_allowance(p):
    return {
        "story": "Here is your monthly allowance, son. Try to make it last the whole month, okay?",
        "npc": "Dad", "avatar": "👨‍🦳",
        "thought": "It's barely enough... I need to budget this carefully.",
        "choices": {
            "Save most": {"cash": +1000, "savings": +3000, "confidence": +3},
            "Spend freely": {"cash": -4000, "confidence": +2, "stress": +2},
            "Split wisely": {"cash": +2500, "savings": +1500}
        }
    }
def stud_insurance(p):
    return {
        "story": "Listen kid, I broke my leg playing football and the bill was huge. You really should get that student health insurance.",
        "npc": "Senior Student", "avatar": "🎓",
        "thought": "₹1200 is a lot of pizza money... but an accident would ruin me.",
        "choices": {
            "Buy insurance": ({"cash": -1200, "insurance": True, "confidence": +4} if p["cash"] >= 1200 else {"stress": +3}),
            "Ignore advice": {"regret": +3}
        }
    }
def stud_exam(p):
    return {
        "story": "This is the final notice. Semester exam fees of ₹3000 are due immediately.",
        "npc": "Admin Office", "avatar": "🏫",
        "thought": "I totally forgot! Where do I get the money now?",
        "choices": {
            "Pay from Cash": {"cash": -3000, "stress": -2},
            "Pay from Savings": {"savings": -3000, "stress": +1},
            "Borrow": {"loan": +3000, "stress": +3}
        }
    }
def stud_phone(p):
    if p["insurance"]:
        return {
            "story": "Ouch! Your screen is shattered. But wait... you have insurance! We'll fix this for free.",
            "npc": "Repair Shop", "avatar": "🛠️",
            "thought": "Thank god I listened to that senior!",
            "auto": {"stress": -4, "insurance": False}
        }
    else:
        return {
            "story": "Ouch! Your screen is shattered. Replacing this display is going to cost you ₹8,000.",
            "npc": "Repair Shop", "avatar": "🛠️",
            "thought": "This is a disaster. I don't have that kind of cash lying around.",
            "choices": {
                "Pay Cash": {"cash": -8000, "stress": +5}, 
                "Take Loan": {"loan": 8000, "stress": +10}
            }
        }
def stud_crypto(p):
    return {
        "story": "Bro! Trust me, 'DogeMoon' is going to the moon! Put in ₹2,000 now and you'll be rich next week!",
        "npc": "Roommate", "avatar": "😎",
        "thought": "He sounds convincing... but this sounds like a scam.",
        "choices": {
            "Invest ₹2000": {"cash": -2000, "regret": 5},
            "Refuse": {"confidence": 5}
        }
    }
def stud_intern(p):
    if p['confidence'] > 50:
        return {
            "story": "We were really impressed by your confidence during the interview. We'd like to offer you a paid internship!",
            "npc": "Recruiter", "avatar": "🤝",
            "thought": "Yes! All that hard work paid off!",
            "auto": {"cash": 10000, "confidence": 10}
        }
    else:
        return {
            "story": "You have good grades, but you seemed very unsure of yourself. We're going with another candidate.",
            "npc": "Recruiter", "avatar": "🤝",
            "thought": "I choked... I need to work on my confidence.",
            "auto": {"stress": 10}
        }

STUDENT_EVENTS = [stud_allowance, stud_insurance, stud_crypto, stud_exam, stud_phone, stud_intern]

# --- ADAPTER ---
def get_event_data(persona, index):
    if persona == "Student":
        if index < len(STUDENT_EVENTS):
            return STUDENT_EVENTS[index](st.session_state.game)
        return None
    if persona in STATIC_CAMPAIGNS:
        campaign = STATIC_CAMPAIGNS[persona]
        if index in campaign:
            raw = campaign[index]
            choices_dict = {}
            for c in raw['choices']:
                effect = c['effects'].copy()
                effect['__msg'] = c['msg'] 
                choices_dict[c['text']] = effect
            return {
                "story": raw['text'], "choices": choices_dict,
                "npc": raw['npc'], "avatar": raw['avatar'],
                "thought": raw.get('thought', "...") # Safety get
            }
    return None

# ==========================================
# 5. RENDER ENGINE
# ==========================================

def get_visuals(story_text, event_data):
    if "avatar" in event_data: return event_data['avatar'], event_data['npc']
    return "🤔", "Inner Voice"

def format_effects(effects):
    """Generates the monetary values only"""
    changes = []
    
    # FILTER: Only show monetary values
    valid_keys = ["cash", "savings", "loan", "investments"]

    for k in valid_keys:
        if k in effects and effects[k] != 0:
            val = effects[k]
            sign = "+" if val > 0 else "-"
            # Format: +₹3,000 Cash
            changes.append(f"{sign}₹{abs(val):,} {k.capitalize()}")
    
    if not changes: return ""
    return f" ({', '.join(changes)})"

def render_scene():
    p = st.session_state.game
    event_data = get_event_data(p['persona'], p['event_index'])
    
    if not event_data:
        p['state'] = "END"
        st.rerun()
        return

    avatar, npc_name = get_visuals(event_data['story'], event_data)
    ins_icon = "🛡️ ACTIVE" if p['insurance'] else "❌ NONE"

    # HUD (Stats Bar) - Includes DEBT
    st.markdown(f"""
    <div class="hud-container">
        <div class="hud-item"><div class="hud-label">ROLE</div><div class="hud-value">{p['persona']}</div></div>
        <div class="hud-item"><div class="hud-label">CASH</div><div class="hud-value money-val">₹{p['cash']:,}</div></div>
        <div class="hud-item"><div class="hud-label">SAVINGS</div><div class="hud-value money-val">₹{p['savings']:,}</div></div>
        <div class="hud-item"><div class="hud-label">DEBT</div><div class="hud-value debt-val">₹{p['loan']:,}</div></div>
        <div class="hud-item"><div class="hud-label">STRESS</div><div class="hud-value stress-val">{p['stress']}%</div></div>
        <div class="hud-item"><div class="hud-label">INSURANCE</div><div class="hud-value">{ins_icon}</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="scene-card">', unsafe_allow_html=True)

    if p['last_feedback']:
        css = f"alert-{p['feedback_type']}"
        st.markdown(f"<div class='game-alert {css}'>{p['last_feedback']}</div>", unsafe_allow_html=True)
        p['last_feedback'] = None

    # DIALOGUE
    st.markdown(f"""
    <div class="dialogue-box">
        <div class="avatar-box">{avatar}</div>
        <div class="speech-bubble">
            <span class="speaker-name">{npc_name}</span>
            {event_data['story']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # THOUGHT BUBBLE
    if "thought" in event_data:
        st.markdown(f"""
        <div class="thought-container">
            <div class="thought-bubble">💭 {event_data['thought']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # CHOICES
    if "choices" in event_data:
        cols = st.columns(len(event_data["choices"]))
        for i, (choice_text, effects) in enumerate(event_data["choices"].items()):
            with cols[i]:
                # Append formatted values (Monetary Only)
                preview_text = format_effects(effects)
                full_label = f"{choice_text} {preview_text}"
                
                if st.button(full_label, key=f"btn_{p['event_index']}_{i}"):
                    custom_msg = effects.pop('__msg', None)
                    success, sys_msg = try_apply_effects(effects)
                    p['last_feedback'] = custom_msg if success and custom_msg else sys_msg
                    p['feedback_type'] = "good" if success else "bad"
                    if success:
                        p['event_index'] += 1
                        p['history'].append(f"{choice_text}")
                    st.rerun()
    elif "auto" in event_data:
        if st.button("Continue ➡️", type="primary"):
            try_apply_effects(event_data["auto"])
            p['last_feedback'] = "Event Processed"
            p['event_index'] += 1
            st.rerun()

# ==========================================
# 6. MAIN LOOP
# ==========================================

if st.session_state.game['state'] == "INTRO":
    st.markdown("<h1 style='text-align:center; font-size: 3rem;'>🌏 Arth-Sagar</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8; margin-bottom: 40px;'>The Ultimate Financial Simulator</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚜 Play Farmer"): 
            st.session_state.game = init_game("Farmer"); st.rerun()
    with c2:
        if st.button("👔 Play Employee"): 
            st.session_state.game = init_game("Employee"); st.rerun()
    with c3:
        if st.button("🎓 Play Student"): 
            st.session_state.game = init_game("Student"); st.rerun()

elif st.session_state.game['state'] == "PLAYING":
    render_sidebar(st.session_state.game) 
    render_scene()

elif st.session_state.game['state'] == "END":
    p = st.session_state.game
    nw = (p['cash'] + p['savings'] + p['investments']) - p['loan']
    st.balloons()
    st.markdown(f"""
    <div style="text-align:center; padding:40px; background: rgba(15, 23, 42, 0.8); border-radius:20px; border: 1px solid #334155; margin-top: 50px;">
        <h1 style='color: #fbbf24;'>Journey Complete: {p['persona']}</h1>
        <h2 style="color:{'#4ade80' if nw>0 else '#f87171'}; font-family: 'Space Mono', monospace;">Net Worth: ₹{nw:,}</h2>
        <div style='display:flex; justify-content:center; gap:20px; margin-top:20px; font-weight:bold;'>
             <span style='color:#f87171'>Debt: ₹{p['loan']:,}</span> | 
             <span style='color:#60a5fa'>Savings: ₹{p['savings']:,}</span> | 
             <span style='color:#c084fc'>Investments: ₹{p['investments']:,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("↺ Restart Journey"):
        st.session_state.game = {"state": "INTRO"}; st.rerun()
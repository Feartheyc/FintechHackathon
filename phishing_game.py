import streamlit as st
import random

# --- SCENARIO DATABASE ---
SCENARIOS = [
    {
        "type": "SMS",
        "sender": "+91 98765 43210",
        "content": "Dear Customer, Your SBI YONO account will be blocked today. Please update your PAN card immediately via: http://sbi-kyc-update.com/login",
        "is_scam": True,
        "explanation": "❌ **SCAM:**\n1. Banks never send KYC links from personal mobile numbers (+91...).\n2. The link is `sbi-kyc-update.com`, NOT `sbi.co.in`.\n3. Creates fake urgency ('blocked today')."
    },
    {
        "type": "SMS",
        "sender": "VM-HDFCBK",
        "content": "Acct XX392 debited with Rs 5000.00 on 12-Feb. Info: ATM WDL. Avl Bal: Rs 12,400. Call 18002026161 if not done by you.",
        "is_scam": False,
        "explanation": "✅ **SAFE:**\n1. Sender ID (VM-HDFCBK) is an official business header.\n2. No suspicious links.\n3. Provides a standard toll-free number for disputes."
    },
    {
        "type": "WhatsApp",
        "sender": "Unknown (+1 202...)",
        "content": "Hey! I am HR from Amazon. We are hiring part-time partners. Daily earn ₹5,000 - ₹10,000. Just like YouTube videos. Click to join: https://wa.me/xyz...",
        "is_scam": True,
        "explanation": "❌ **SCAM:**\n1. Big companies don't hire via random WhatsApp messages.\n2. International number (+1...) for an Indian job.\n3. 'Like videos to earn money' is a classic Ponzi scam."
    },
    {
        "type": "Browser",
        "sender": "Address Bar",
        "content": "https://www.amaz0n-big-sale.shop/iphone15",
        "is_scam": True,
        "explanation": "❌ **SCAM:**\n1. Look closely: it spells `amaz0n` (Zero instead of O).\n2. Domain ends in `.shop`, not `.in` or `.com`.\n3. Too good to be true offers are usually phishing."
    },
    {
        "type": "Call",
        "sender": "Caller: 'Bank Manager'",
        "content": "(Voice Transcript): 'Sir, I am calling from your bank. Someone is trying to hack your account. I have sent an OTP to your phone. Please verify it to stop the hack.'",
        "is_scam": True,
        "explanation": "❌ **SCAM:**\n1. Bank officials **NEVER** ask for OTPs over the call.\n2. Fear tactic ('hacking') used to make you panic.\n3. OTPs are for *transactions*, not for 'stopping' hacks."
    }
]

def init_cyber_game():
    if "cyber_q_index" not in st.session_state:
        st.session_state.cyber_q_index = 0
        st.session_state.cyber_score = 0

def render_phishing_game():
    init_cyber_game()
    
    # Custom CSS for Phone UI
    st.markdown("""
    <style>
        .phone-frame {
            background: #000000;
            border-radius: 30px;
            padding: 15px;
            max-width: 400px;
            margin: 0 auto;
            border: 4px solid #333;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        .phone-screen {
            background: #f0f2f5;
            border-radius: 20px;
            min-height: 400px;
            padding: 20px;
            color: #1f2937;
            font-family: sans-serif;
            position: relative;
        }
        .msg-bubble {
            background: #ffffff;
            padding: 15px;
            border-radius: 0 15px 15px 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-top: 10px;
            border: 1px solid #e5e7eb;
        }
        .sender-id {
            font-weight: bold;
            font-size: 0.9rem;
            color: #374151;
            margin-bottom: 5px;
        }
        .msg-meta {
            font-size: 0.7rem;
            color: #9ca3af;
            text-align: right;
            margin-top: 5px;
        }
        .browser-bar {
            background: #e5e7eb;
            padding: 8px 15px;
            border-radius: 20px;
            margin-bottom: 20px;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            color: #374151;
        }
        .lock-icon { margin-right: 8px; color: #059669; }
        .cyber-stats {
            text-align: center; 
            margin-bottom: 20px; 
            padding: 10px; 
            background: rgba(16, 185, 129, 0.1); 
            border-radius: 10px;
            border: 1px solid #059669;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Header ---
    st.markdown("<h1 style='text-align:center;'>🛡️ Cyber Shield</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>Real or Fake? Test your detection skills.</p>", unsafe_allow_html=True)

    # --- Scoreboard ---
    st.markdown(f"""
    <div class="cyber-stats">
        <span style="font-size: 1.2rem; font-weight:bold; color: #34d399;">
            Score: {st.session_state.cyber_score} / {len(SCENARIOS)}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # --- Game Logic ---
    if st.session_state.cyber_q_index < len(SCENARIOS):
        q = SCENARIOS[st.session_state.cyber_q_index]
        
        # --- RENDER PHONE INTERFACE ---
        screen_content = ""
        if q['type'] == "Browser":
            screen_content = f"""
            <div class="browser-bar">
                <span class="lock-icon">🔒</span> {q['content']}
            </div>
            <div style="text-align:center; margin-top:50px; color:#9ca3af;">
                <h2 style="color:#1f2937">Web Page Loaded...</h2>
                <p>Limited Time Offer!</p>
            </div>
            """
        else:
            icon = "💬" if q['type'] == "SMS" else ("📞" if q['type'] == "Call" else "📱")
            screen_content = f"""
            <div style="text-align:center; margin-bottom:20px; color:#6b7280; font-size:0.8rem;">
                Today, 10:42 AM
            </div>
            <div class="sender-id">{icon} {q['sender']}</div>
            <div class="msg-bubble">
                {q['content']}
                <div class="msg-meta">Now</div>
            </div>
            """

        st.markdown(f"""
        <div class="phone-frame">
            <div class="phone-screen">
                {screen_content}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- CONTROLS ---
        st.write("")
        c1, c2 = st.columns(2)
        
        with c1:
            if st.button("✅ It's REAL", use_container_width=True):
                check_answer(q, user_said_scam=False)
        with c2:
            if st.button("🚨 It's a SCAM", type="primary", use_container_width=True):
                check_answer(q, user_said_scam=True)

    else:
        # Game Over Screen
        st.markdown("""
        <div class="scene-card" style="text-align:center; padding:40px;">
            <h2 style="color:#facc15;">Training Complete!</h2>
            <p>You are now sharper against digital fraud.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.cyber_q_index = 0
            st.session_state.cyber_score = 0
            st.rerun()
        if st.button("⬅ Return to Main Menu", use_container_width=True):
            st.session_state.game['state'] = "INTRO"
            st.rerun()

def check_answer(question, user_said_scam):
    is_correct = (user_said_scam == question['is_scam'])
    
    if is_correct:
        st.session_state.cyber_score += 1
        msg = "🎉 Correct! Good eye."
    else:
        msg = "⚠️ Oops! That was a mistake."
    
    @st.dialog("Analysis Result")
    def show_result():
        if is_correct:
            st.success(msg)
        else:
            st.error(msg)
        
        st.markdown(f"### {question['explanation']}")
        if st.button("Next Scenario ➡️"):
            st.session_state.cyber_q_index += 1
            st.rerun()
            
    show_result()
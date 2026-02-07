import streamlit as st
import random

# --- EXPANDED COMPARISON DATABASE ---
MASTER_SCENARIOS = [
    # --- TYPE: SMS / WHATSAPP ---
    {
        "id": "sms_electricity",
        "type": "SMS",
        "scenario": "Urgent Electricity Bill",
        "option_a": {
            "type": "scam",
            "sender": "+91 90210...",
            "content": "Dear Consumer, Your electricity power will be disconnected TONIGHT at 9:30 PM because previous bill is not update. Call immediately our officer 88XXX...",
            "reason": "Electricity boards never cut power at night via personal SMS threats. They send official notices."
        },
        "option_b": {
            "type": "safe",
            "sender": "MSEDCL",
            "content": "Bill for Consumer No. 00012345678 is Rs 1,240. Due Date: 15-Mar. Please pay via official website or app to avoid penalty.",
            "reason": "Official sender ID, specific details (Consumer No), and no threat of immediate disconnection."
        }
    },
    {
        "id": "sms_job",
        "type": "WhatsApp",
        "scenario": "Part-Time Job Offer",
        "option_a": {
            "type": "safe",
            "sender": "LinkedIn Info",
            "content": "Hi, your profile appeared in a search by a recruiter at TechSol. Tap to view the job details in the LinkedIn app.",
            "reason": "Notification directs you to a trusted platform (LinkedIn) rather than asking for direct contact."
        },
        "option_b": {
            "type": "scam",
            "sender": "Unknown (+1 234...)",
            "content": "Hello! Earn ₹5,000-₹10,000 daily working from home. Simple task: Like YouTube videos. Join Telegram: t.me/fake_job...",
            "reason": "International number (+1), 'Like videos to earn' is a classic Ponzi scam pattern."
        }
    },
    
    # --- TYPE: BROWSER / LINKS ---
    {
        "id": "link_bank",
        "type": "Browser",
        "scenario": "Bank KYC Update",
        "option_a": {
            "type": "safe",
            "sender": "hdfcbank.com",
            "content": "https://www.hdfcbank.com/personal/ways-to-bank/mobile-banking",
            "reason": "Correct domain spelling (`hdfcbank.com`). Uses HTTPS and standard structure."
        },
        "option_b": {
            "type": "scam",
            "sender": "hdfc-kyc-update.net",
            "content": "http://hdfc-kyc-update.net/login/verify-pan",
            "reason": "Fake domain (`hdfc-kyc-update.net`). Banks host everything on their main domain. Uses HTTP (insecure)."
        }
    },
    {
        "id": "link_shopping",
        "type": "Browser",
        "scenario": "Flash Sale Offer",
        "option_a": {
            "type": "scam",
            "sender": "amaz0n-sale.shop",
            "content": "https://www.amaz0n-big-billion.shop/iphone15-90off",
            "reason": "Look closely: `amaz0n` (Zero instead of O). Domain ends in `.shop` instead of `.in` or `.com`."
        },
        "option_b": {
            "type": "safe",
            "sender": "amazon.in",
            "content": "https://www.amazon.in/events/great-indian-festival",
            "reason": "Correct official domain `amazon.in`."
        }
    },
    {
        "id": "link_irctc",
        "type": "Browser",
        "scenario": "Ticket Refund",
        "option_a": {
            "type": "scam",
            "sender": "irctc-refunds.com",
            "content": "https://irctc-refunds.com/claim-money",
            "reason": "IRCTC refunds are automatic. They never ask you to visit a separate link to 'claim' money."
        },
        "option_b": {
            "type": "safe",
            "sender": "irctc.co.in",
            "content": "https://www.irctc.co.in/nget/booking/refund-history",
            "reason": "Official IRCTC domain."
        }
    },

    # --- TYPE: CALL TRANSCRIPTS ---
    {
        "id": "call_arrest",
        "type": "Call",
        "scenario": "Digital Arrest / Fedex Scam",
        "option_a": {
            "type": "scam",
            "sender": "Unknown Caller",
            "content": "Transcript: 'This is Mumbai Police. A parcel with drugs was seized in your name. We are doing a Skype interrogation. Transfer ₹50k to RBI safe account to verify funds or you will be arrested.'",
            "reason": "Police NEVER do 'Skype interrogations' and NEVER ask you to transfer money to a 'safe account'."
        },
        "option_b": {
            "type": "safe",
            "sender": "Police Station",
            "content": "Transcript: 'Sir, this is Sub-Inspector Patil. A complaint has been filed. Please visit the Andheri East station tomorrow morning with your ID proof.'",
            "reason": "Real police ask you to come to the station physically. They don't threaten arrest via video call."
        }
    },
    {
        "id": "call_refund",
        "type": "Call",
        "scenario": "Wrong Refund Scam",
        "option_a": {
            "type": "safe",
            "sender": "Amazon Support",
            "content": "Transcript: 'Sir, we processed your refund for the damaged item. It will reflect in your original payment source within 3-5 business days.'",
            "reason": "Standard procedure. No action required from you."
        },
        "option_b": {
            "type": "scam",
            "sender": "Customer Care",
            "content": "Transcript: 'Sir, we are trying to refund you but your GPay is locked. I sent a QR code. Please scan it and enter your UPI PIN to RECEIVE money.'",
            "reason": "You NEVER enter a UPI PIN to receive money. PIN is only for sending money."
        }
    },
    {
        "id": "call_family",
        "type": "Call",
        "scenario": "Family Emergency (AI Voice)",
        "option_a": {
            "type": "scam",
            "sender": "Unknown Number",
            "content": "Transcript: (Crying Voice) 'Dad! I got into an accident with a VIP car. They are beating me. Send ₹20,000 to this number immediately or they will call police!'",
            "reason": "Classic 'Emergency Scam'. Scammers create panic so you don't think. Always call your relative's actual number to verify."
        },
        "option_b": {
            "type": "safe",
            "sender": "Son (Saved Contact)",
            "content": "Transcript: 'Hey Dad, just calling to say I reached the hostel safely. Will call you properly after dinner.'",
            "reason": "Normal conversation from a saved contact."
        }
    },
    {
        "id": "call_credit",
        "type": "Call",
        "scenario": "Credit Card Points",
        "option_a": {
            "type": "scam",
            "sender": "Bank Rep",
            "content": "Transcript: 'Ma'am your 5000 credit points are expiring today. Give me your card number and OTP to convert them into Cash.'",
            "reason": "Banks never ask for OTP or Card Number to redeem points. Points are redeemed via net banking only."
        },
        "option_b": {
            "type": "safe",
            "sender": "Relationship Mgr",
            "content": "Transcript: 'Sir, this is your RM. Just informing you that your card limit can be increased. Check the offer in your mobile app if interested.'",
            "reason": "Directs you to the official app. Does not ask for sensitive info over call."
        }
    },
     {
        "id": "sms_lottery",
        "type": "SMS",
        "scenario": "Lottery Win",
        "option_a": {
            "type": "scam",
            "sender": "Winner",
            "content": "Congrats! You won Rs 25 Lakh in KBC Lottery. Contact Rana Pratap 88XXXXX. Pay Rs 5000 tax to claim.",
            "reason": "You cannot win a lottery you didn't enter. You never pay money to get money."
        },
        "option_b": {
            "type": "safe",
            "sender": "IT-DEPT",
            "content": "Your Income Tax Refund of Rs 2,500 for AY 2025-26 has been processed. It will credit to XX1234 shortly.",
            "reason": "Official notification. No demand for payment."
        }
    },
]

def init_cyber_game():
    if "cyber_deck" not in st.session_state or not st.session_state.cyber_deck:
        st.session_state.cyber_score = 0
        st.session_state.cyber_total = 5
        
        shuffled_scenarios = MASTER_SCENARIOS.copy()
        random.shuffle(shuffled_scenarios)
        
        selected_scenarios = shuffled_scenarios[:5]
        
        deck = []
        for s in selected_scenarios:
            order = ["option_a", "option_b"]
            random.shuffle(order)
            deck.append({
                "data": s,
                "order": order
            })
        
        st.session_state.cyber_deck = deck
        st.session_state.cyber_current_idx = 0

def render_phone_screen(data, display_type):
    """Renders a single phone screen UI based on type"""
    
    sender = data['sender']
    content = data['content']
    
    # --- FIXED: NO INDENTATION IN HTML STRINGS ---
    
    if display_type == "Browser":
        inner_html = f"""
<div class="browser-bar">
<span style="color:#10b981; margin-right:5px;">🔒</span> {sender}
</div>
<div class="browser-content">
<div style="font-size:0.8rem; color:#64748b; margin-bottom:10px;">{content}</div>
<div style="background:#e2e8f0; height:80px; width:100%; border-radius:4px; margin-bottom:10px;"></div>
<div style="background:#e2e8f0; height:10px; width:60%; border-radius:2px;"></div>
</div>
"""
        
    elif display_type == "Call":
        inner_html = f"""
<div class="call-header">
<div style="font-size:2rem;">👤</div>
<div style="font-weight:bold; color:#1e293b;">{sender}</div>
<div style="font-size:0.7rem; color:#ef4444;">• Rec 00:45</div>
</div>
<div class="transcript-box">
{content}
</div>
<div style="text-align:center; margin-top:10px;">
<span style="font-size:1.5rem;">🔇 📞 🔊</span>
</div>
"""
        
    else:
        # SMS / WhatsApp
        icon = "💬" if display_type == "SMS" else "🟢"
        inner_html = f"""
<div class="top-bar">Today, 10:42 AM</div>
<div class="sender-id">{icon} {sender}</div>
<div class="msg-bubble">
{content}
<div class="msg-meta">Now</div>
</div>
"""

    # RENDER FRAME (NO INDENTATION)
    st.markdown(f"""
<div class="phone-frame">
<div class="phone-screen">
{inner_html}
</div>
</div>
""", unsafe_allow_html=True)

def render_phishing_game():
    init_cyber_game()
    
    st.markdown("""
    <style>
        .phone-frame {
            background: #1e293b;
            border-radius: 20px;
            padding: 10px;
            border: 4px solid #334155;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            max-width: 320px;
            margin: 0 auto;
        }
        .phone-screen {
            background: #f8fafc;
            border-radius: 15px;
            min-height: 300px;
            padding: 15px;
            color: #1e293b;
            font-family: sans-serif;
            font-size: 0.9rem;
            position: relative;
            display: flex;
            flex-direction: column;
        }
        
        /* SMS Styles */
        .top-bar { text-align: center; font-size: 0.7rem; color: #94a3b8; margin-bottom: 10px; }
        .sender-id { font-weight: bold; font-size: 0.9rem; margin-bottom: 5px; color: #0f172a; }
        .msg-bubble { background: #ffffff; padding: 12px; border-radius: 0 12px 12px 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; line-height: 1.4; }
        .msg-meta { text-align: right; font-size: 0.65rem; color: #cbd5e1; margin-top: 5px; }
        
        /* Browser Styles */
        .browser-bar { background: #e2e8f0; padding: 8px; border-radius: 8px; font-size: 0.75rem; color: #334155; font-weight:bold; margin-bottom: 15px; border: 1px solid #cbd5e1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .browser-content { text-align: center; }
        
        /* Call Styles */
        .call-header { text-align: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #e2e8f0; }
        .transcript-box { background: #fff1f2; color: #881337; padding: 10px; border-radius: 8px; font-size: 0.8rem; font-style: italic; border-left: 3px solid #f43f5e; }

        .vs-badge { text-align: center; font-size: 2rem; font-weight: 800; color: #facc15; margin-top: 120px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>🛡️ Cyber Shield</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#94a3b8;'>Scenario {st.session_state.cyber_current_idx + 1} of {st.session_state.cyber_total} | Score: {st.session_state.cyber_score}</p>", unsafe_allow_html=True)

    if st.session_state.cyber_current_idx < st.session_state.cyber_total:
        
        current_item = st.session_state.cyber_deck[st.session_state.cyber_current_idx]
        q_data = current_item['data']
        order = current_item['order']
        
        item_1 = q_data[order[0]]
        item_2 = q_data[order[1]]
        scen_type = q_data['type']

        st.markdown(f"<h3 style='text-align:center; margin-bottom:30px; color:#38bdf8;'>Category: {scen_type}</h3>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 0.2, 1])
        
        with c1:
            st.markdown("<div style='text-align:center; font-weight:bold; margin-bottom:10px; color:#94a3b8'>Option A</div>", unsafe_allow_html=True)
            render_phone_screen(item_1, scen_type)
            st.write("")
            if st.button("✅ Pick Option A", key="btn_left", use_container_width=True):
                check_selection(item_1)

        with c2:
            st.markdown('<div class="vs-badge">VS</div>', unsafe_allow_html=True)

        with c3:
            st.markdown("<div style='text-align:center; font-weight:bold; margin-bottom:10px; color:#94a3b8'>Option B</div>", unsafe_allow_html=True)
            render_phone_screen(item_2, scen_type)
            st.write("")
            if st.button("✅ Pick Option B", key="btn_right", use_container_width=True):
                check_selection(item_2)

    else:
        st.markdown(f"""
        <div class="scene-card" style="text-align:center; padding:40px;">
            <h2 style="color:#facc15;">Training Session Complete!</h2>
            <h1 style="font-size:3rem;">{st.session_state.cyber_score} / {st.session_state.cyber_total}</h1>
            <p>You have improved your fraud detection skills.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Start New Training (New Mix)", use_container_width=True):
            st.session_state.cyber_deck = []
            st.rerun()
        if st.button("⬅ Return to Main Menu", use_container_width=True):
            st.session_state.game['state'] = "MAIN_MENU"
            st.rerun()

def check_selection(selected_item):
    is_safe = (selected_item['type'] == "safe")
    
    if is_safe:
        st.session_state.cyber_score += 1
        title = "🎉 Correct!"
        msg = f"**Well done!**\n\n{selected_item['reason']}"
    else:
        title = "⚠️ Caught by Scam!"
        msg = f"**You picked the SCAM.**\n\nReason: {selected_item['reason']}"

    @st.dialog(title)
    def show_feedback():
        if is_safe:
            st.success(msg)
        else:
            st.error(msg)
        
        if st.button("Next Scenario ➡️"):
            st.session_state.cyber_current_idx += 1
            st.rerun()
    
    show_feedback()
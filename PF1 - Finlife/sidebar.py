import streamlit as st

# -----------------------------
# SCHEMES DATABASE (Rural-Friendly)
# -----------------------------
SCHEMES = {
    "Student": [
        {
            "name": "Vidya Lakshmi Portal",
            "desc": "Govt pays your loan interest while you study. No worry about paying back immediately.",
            "condition": lambda p: p['cash'] < 5000, 
            "levels": [0, 1, 2],
            "effects": {"cash": 5000}
        },
        {
            "name": "PM Scholarship",
            "desc": "Free money for students with good marks. You don't have to pay this back.",
            "condition": lambda p: p['confidence'] >= 50, 
            "levels": [0, 3, 5],
            "effects": {"savings": 5000, "confidence": 5}
        },
        {
            "name": "Ayushman Bharat",
            "desc": "Free hospital treatment card up to ₹5 Lakhs for your family.",
            "condition": lambda p: not p['insurance'], 
            "levels": [1, 4],
            "effects": {"insurance": True}
        },
        {
            "name": "Digital India Skill",
            "desc": "Learn computer skills for free to get better part-time jobs.",
            "condition": lambda p: p['cash'] >= 1000, 
            "levels": [2],
            "effects": {"confidence": 3}
        },
    ],
    "Farmer": [
        {
            "name": "Kisan Credit Card (KCC)",
            "desc": "Get a bank loan at very low interest (4-7%) for seeds and fertilizers.",
            "condition": lambda p: p['loan'] < 50000, 
            "levels": [0, 3],
            "effects": {"cash": 20000, "loan": 20000}
        },
        {
            "name": "PM Fasal Bima Yojana",
            "desc": "Crop Insurance. If rain or pests destroy your crop, the government pays you.",
            "condition": lambda p: not p['insurance'], 
            "levels": [0, 2, 4],
            "effects": {"insurance": True}
        },
        {
            "name": "Fertilizer Subsidy",
            "desc": "Get Urea and DAP fertilizers at a huge discount directly from the shop.",
            "condition": lambda p: True, 
            "levels": [0, 1, 2, 3],
            "effects": {"savings": 3000}
        },
        {
            "name": "PM Kisan Tractor",
            "desc": "Get 20-50% money help (subsidy) from govt to buy a new tractor.",
            "condition": lambda p: p['loan'] < 500000, 
            "levels": [5],
            "effects": {"loan": 500000}
        },
        {
            "name": "e-NAM Market",
            "desc": "Check the real price of crops on your phone so middlemen can't cheat you.",
            "condition": lambda p: True, 
            "levels": [2],
            "effects": {"confidence": 5}
        },
        {
            "name": "PM Krishi Sinchai",
            "desc": "Money help for installing drip irrigation or sprinklers to save water.",
            "condition": lambda p: p['cash'] < 10000, 
            "levels": [1, 3],
            "effects": {"cash": 5000}
        },
    ],
    "Employee": [
        {
            "name": "EPF (Provident Fund)",
            "desc": "Automatic savings from your salary for old age. Govt gives interest on it.",
            "condition": lambda p: True, 
            "levels": [0, 2, 3, 5],
            "effects": {"savings": 10000}
        },
        {
            "name": "ESIC Health Card",
            "desc": "Full medical treatment for you and family at very low cost.",
            "condition": lambda p: not p['insurance'], 
            "levels": [4],
            "effects": {"insurance": True}
        },
        {
            "name": "PM Kaushal Vikas",
            "desc": "Free training to learn new technical skills and get a promotion.",
            "condition": lambda p: p['confidence'] < 50, 
            "levels": [1, 3, 6],
            "effects": {"confidence": 5}
        },
        {
            "name": "PMAY (Awas Yojana)",
            "desc": "Money help from govt to build or buy your first pucca house.",
            "condition": lambda p: True, 
            "levels": [2, 5],
            "effects": {"cash": 20000}
        },
    ],
    "Founder": [
    {
        "name": "Startup India Seed Fund",
        "desc": "Govt gives money to start your business idea without taking shares.",
        "condition": lambda p: p['cash'] < 50000,
        "levels": [0, 1],
        "effects": {"cash": 50000, "confidence": 10}
    },
    {
        "name": "MUDRA Loan",
        "desc": "Easy business loan up to ₹10 Lakhs without keeping your house as guarantee.",
        "condition": lambda p: p['loan'] == 0,
        "levels": [1, 2, 3],
        "effects": {"cash": 100000, "loan": 100000}
    },
    {
        "name": "Tax Holiday",
        "desc": "You don't have to pay Income Tax for the first 3 years of profit.",
        "condition": lambda p: True,
        "levels": [3, 4, 5],
        "effects": {"savings": 20000}
    },
    {
        "name": "Angel Investor Boost",
        "desc": "An angel investor offers ₹20 Lakhs for 10% equity.",
        "condition": lambda p: p['confidence'] > 10,
        "levels": [2, 3],
        "effects": {"cash": 2000000, "confidence": 15, "equity": -10}
    },
    {
        "name": "Government R&D Grant",
        "desc": "Govt provides grant for product innovation and tech development.",
        "condition": lambda p: p['tech_skill'] >= 5,
        "levels": [1, 2, 3],
        "effects": {"cash": 500000, "tech_skill": 2}
    },
    {
        "name": "Incubator Support",
        "desc": "Get mentorship, workspace, and initial seed funding from an incubator.",
        "condition": lambda p: p['stress'] < 50,
        "levels": [0, 1, 2],
        "effects": {"cash": 200000, "confidence": 10, "stress": -10}
    },
    {
        "name": "Equity Crowdfunding",
        "desc": "Raise small amounts from multiple investors via crowdfunding platforms.",
        "condition": lambda p: p['cash'] < 200000,
        "levels": [3, 4],
        "effects": {"cash": 1000000, "stress": 5, "equity": -5}
    },
    {
        "name": "Startup Accelerator",
        "desc": "Join a 3-month accelerator to get guidance, networking, and funding.",
        "condition": lambda p: p['cash'] < 100000,
        "levels": [1, 2, 3],
        "effects": {"cash": 300000, "confidence": 15, "stress": 10}
    },
    {
        "name": "Government Export Incentive",
        "desc": "Receive incentives for selling products internationally.",
        "condition": lambda p: p['level'] >= 5,
        "levels": [5, 6, 7],
        "effects": {"cash": 1000000, "confidence": 10}
    }
]
}

# -----------------------------
# SIDEBAR RENDER FUNCTION
# -----------------------------
def render_sidebar(game_state):
    st.sidebar.markdown("### 🏛️ Govt Schemes")
    st.sidebar.markdown("<small>Schemes available for you right now:</small>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    if "persona" not in game_state:
        st.sidebar.info("Start a journey to see available schemes.")
        return

    # Initialize claimed schemes & feedback
    if "claimed_schemes" not in game_state:
        game_state["claimed_schemes"] = []
    if "last_scheme_feedback" not in game_state:
        game_state["last_scheme_feedback"] = None

    persona = game_state['persona']
    level = game_state.get("event_index", 0)

    # Filter Eligible Schemes
    eligible_schemes = []
    for scheme in SCHEMES.get(persona, []):
        try:
            if (
                level in scheme.get("levels", [])
                and scheme['condition'](game_state)
                and scheme['name'] not in game_state["claimed_schemes"]
            ):
                eligible_schemes.append(scheme)
        except KeyError:
            continue

    if eligible_schemes:
        for i, scheme in enumerate(eligible_schemes):
            # VISUAL CARD FOR SCHEME
            with st.sidebar.container():
                st.markdown(f"**{scheme['name']}**")
                st.caption(f"ℹ️ {scheme['desc']}") # The simple rural explanation
                
                if st.button(f"✅ Claim Benefit", key=f"claim_{i}_{scheme['name']}", use_container_width=True):
                    # Apply scheme effects
                    for k, v in scheme.get("effects", {}).items():
                        if k in game_state:
                            game_state[k] += v if isinstance(v, (int, float)) else 0
                        elif k == "insurance":
                            game_state["insurance"] = v

                    game_state["claimed_schemes"].append(scheme['name'])

                    # Set feedback text
                    feedback_parts = []
                    for k, v in scheme.get("effects", {}).items():
                        if isinstance(v, (int, float)):
                            feedback_parts.append(f"₹{v:,} added to {k}")
                        elif k == "insurance":
                            feedback_parts.append(f"Insurance ACTIVE")
                    game_state["last_scheme_feedback"] = f"🎉 {scheme['name']} Approved! {'; '.join(feedback_parts)}"

                    st.rerun()
                st.markdown("---") # Separator between schemes

    else:
        st.sidebar.info("No new schemes available at this level. Keep playing!")

    # Display scheme feedback if any
    if game_state.get("last_scheme_feedback"):
        st.toast(game_state["last_scheme_feedback"], icon="🎉")
        # Reset feedback after showing
        game_state["last_scheme_feedback"] = None
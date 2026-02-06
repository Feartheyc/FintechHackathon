import streamlit as st

# -----------------------------
# SCHEMES DATABASE (LEVEL BASED, EXPANDED)
# -----------------------------
SCHEMES = {
    "Student": [
        {"name": "Student Loan Subsidy", "condition": lambda p: p['cash'] < 5000, "levels": [0, 1, 2],
         "effects": {"cash": 5000}},
        {"name": "Merit Scholarship", "condition": lambda p: p['confidence'] >= 50, "levels": [0, 3, 5],
         "effects": {"savings": 5000, "confidence": 5}},
        {"name": "Health Insurance Subsidy", "condition": lambda p: not p['insurance'], "levels": [1, 4],
         "effects": {"insurance": True}},
        {"name": "Crypto Awareness Workshop", "condition": lambda p: p['cash'] >= 1000, "levels": [2],
         "effects": {"confidence": 3}},
        {"name": "Internship Booster Grant", "condition": lambda p: p['confidence'] >= 60, "levels": [5],
         "effects": {"cash": 8000, "confidence": 5}},
        {"name": "Library Membership Discount", "condition": lambda p: p['cash'] >= 500, "levels": [1, 2, 3],
         "effects": {"cash": -500, "confidence": 2}},
        {"name": "Scholarship Guidance Program", "condition": lambda p: p['confidence'] < 60, "levels": [0, 4],
         "effects": {"confidence": 4}},
    ],
    "Farmer": [
        {"name": "KCC Loan", "condition": lambda p: p['loan'] < 50000, "levels": [0, 3],
         "effects": {"cash": 20000, "loan": 20000}},
        {"name": "Crop Insurance", "condition": lambda p: not p['insurance'], "levels": [0, 2, 4],
         "effects": {"insurance": True}},
        {"name": "Fertilizer Subsidy", "condition": lambda p: True, "levels": [0, 1, 2, 3],
         "effects": {"savings": 3000}},
        {"name": "Tractor Loan Support", "condition": lambda p: p['loan'] < 500000, "levels": [5],
         "effects": {"loan": 500000}},
        {"name": "Market Price Alert", "condition": lambda p: True, "levels": [2],
         "effects": {"confidence": 5}},
        {"name": "Irrigation Subsidy", "condition": lambda p: p['cash'] < 10000, "levels": [1, 3],
         "effects": {"cash": 5000}},
        {"name": "Seed Quality Grant", "condition": lambda p: p.get("flags", {}).get("hybrid_seeds", False), "levels": [1],
         "effects": {"savings": 2000}},
    ],
    "Employee": [
        {"name": "PF Contribution Bonus", "condition": lambda p: True, "levels": [0, 2, 3, 5],
         "effects": {"savings": 10000}},
        {"name": "Medical Insurance Scheme", "condition": lambda p: not p['insurance'], "levels": [4],
         "effects": {"insurance": True}},
        {"name": "Skill Development Program", "condition": lambda p: p['confidence'] < 50, "levels": [1, 3, 6],
         "effects": {"confidence": 5}},
        {"name": "Salary Advance Option", "condition": lambda p: p['cash'] < 20000, "levels": [0, 1, 2],
         "effects": {"cash": 10000, "loan": 5000}},
        {"name": "Housing Allowance", "condition": lambda p: True, "levels": [2, 5],
         "effects": {"cash": 20000}},
        {"name": "Transport Subsidy", "condition": lambda p: p['loan'] > 0, "levels": [2, 3],
         "effects": {"cash": 5000}},
        {"name": "Health Check-up Voucher", "condition": lambda p: p['stress'] > 50, "levels": [4, 6],
         "effects": {"stress": -10}},
    ]
}

# -----------------------------
# SIDEBAR RENDER FUNCTION
# -----------------------------
def render_sidebar(game_state):
    st.sidebar.markdown("### 🌏 Game Sidebar")

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
    st.sidebar.markdown(f"### 🌏 {persona} - Eligible Schemes (Level {level})")

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
        for scheme in eligible_schemes:
            if st.sidebar.button(f"Claim {scheme['name']}"):
                # Apply scheme effects
                for k, v in scheme.get("effects", {}).items():
                    if k in game_state:
                        game_state[k] += v if isinstance(v, (int, float)) else 0
                    elif k == "insurance":
                        game_state["insurance"] = v

                game_state["claimed_schemes"].append(scheme['name'])

                # Set sidebar feedback
                feedback_parts = []
                for k, v in scheme.get("effects", {}).items():
                    if isinstance(v, (int, float)):
                        feedback_parts.append(f"₹{v:,} added to {k}")
                    elif k == "insurance":
                        feedback_parts.append(f"Insurance ACTIVE")
                game_state["last_scheme_feedback"] = f"✅ {scheme['name']} claimed! {'; '.join(feedback_parts)}"

                st.rerun()

    else:
        st.sidebar.info("No schemes currently available for your status.")

    # Display scheme feedback if any
    if game_state.get("last_scheme_feedback"):
        st.sidebar.success(game_state["last_scheme_feedback"])
        # Reset feedback after showing
        game_state["last_scheme_feedback"] = None

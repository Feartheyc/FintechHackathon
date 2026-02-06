import streamlit as st

# -----------------------------
# SCHEMES DATABASE (LEVEL BASED, EXPANDED)
# -----------------------------
SCHEMES = {
    "Student": [
        {"name": "Student Loan Subsidy", "condition": lambda p: p['cash'] < 5000, "levels": [0, 1, 2]},
        {"name": "Merit Scholarship", "condition": lambda p: p['confidence'] >= 50, "levels": [0, 3, 5]},
        {"name": "Health Insurance Subsidy", "condition": lambda p: not p['insurance'], "levels": [1, 4]},
        {"name": "Crypto Awareness Workshop", "condition": lambda p: p['cash'] >= 1000, "levels": [2]},
        {"name": "Internship Booster Grant", "condition": lambda p: p['confidence'] >= 60, "levels": [5]},
        {"name": "Library Membership Discount", "condition": lambda p: p['cash'] >= 500, "levels": [1, 2, 3]},
        {"name": "Scholarship Guidance Program", "condition": lambda p: p['confidence'] < 60, "levels": [0, 4]},
    ],
    "Farmer": [
        {"name": "KCC Loan", "condition": lambda p: p['loan'] < 50000, "levels": [0, 3]},
        {"name": "Crop Insurance", "condition": lambda p: not p['insurance'], "levels": [0, 2, 4]},
        {"name": "Fertilizer Subsidy", "condition": lambda p: True, "levels": [0, 1, 2, 3]},
        {"name": "Tractor Loan Support", "condition": lambda p: p['loan'] < 500000, "levels": [5]},
        {"name": "Market Price Alert", "condition": lambda p: True, "levels": [2]},
        {"name": "Irrigation Subsidy", "condition": lambda p: p['cash'] < 10000, "levels": [1, 3]},
        {"name": "Seed Quality Grant", "condition": lambda p: p.get("flags", {}).get("hybrid_seeds", False), "levels": [1]},
    ],
    "Employee": [
        {"name": "PF Contribution Bonus", "condition": lambda p: True, "levels": [0, 2, 3, 5]},
        {"name": "Medical Insurance Scheme", "condition": lambda p: not p['insurance'], "levels": [4]},
        {"name": "Skill Development Program", "condition": lambda p: p['confidence'] < 50, "levels": [1, 3, 6]},
        {"name": "Salary Advance Option", "condition": lambda p: p['cash'] < 20000, "levels": [0, 1, 2]},
        {"name": "Housing Allowance", "condition": lambda p: True, "levels": [2, 5]},
        {"name": "Transport Subsidy", "condition": lambda p: p['loan'] > 0, "levels": [2, 3]},
        {"name": "Health Check-up Voucher", "condition": lambda p: p['stress'] > 50, "levels": [4, 6]},
    ]
}

# -----------------------------
# SIDEBAR RENDER FUNCTION
# -----------------------------
def render_sidebar(game_state):

    if "persona" not in game_state:
        st.sidebar.info("Start a journey to see available schemes.")
        return

    persona = game_state['persona']
    level = game_state.get("event_index", 0)
    st.sidebar.markdown(f"### 🌏 {persona} - Eligible Schemes (Level {level})")

    eligible_schemes = []
    for scheme in SCHEMES.get(persona, []):
        try:
            if level in scheme.get("levels", []) and scheme['condition'](game_state):
                eligible_schemes.append(scheme['name'])
        except KeyError:
            continue

    if eligible_schemes:
        for s in eligible_schemes:
            st.sidebar.success(f"✅ {s}")
    else:
        st.sidebar.info("No schemes currently available for your status.")

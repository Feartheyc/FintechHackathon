import streamlit as st

# ---------------- INIT PLAYER STATE ----------------
def init_state():
    return {
        "event_index": 0,
        "cash": 6000,
        "savings": 2000,
        "loan": 0,
        "investments": 0,
        "insurance": False,
        "confidence": 50,
        "stress": 25,
        "regret": 0,
        "history": []
    }

if "player" not in st.session_state:
    st.session_state.player = init_state()

player = st.session_state.player

# ---------------- HELPER ----------------
def apply_effects(effects):
    for k, v in effects.items():
        player[k] += v

# ---------------- EVENTS ----------------
def allowance_event(p):
    return {
        "story": "You receive your first monthly allowance.",
        "choices": {
            "Save most of it": {"cash": +1000, "savings": +3000, "confidence": +3},
            "Spend freely": {"cash": +4000, "confidence": +2, "stress": +2},
            "Split wisely": {"cash": +2500, "savings": +1500}
        }
    }

def insurance_event(p):
    return {
        "story": "A senior advises you to get health insurance.",
        "choices": {
            "Buy insurance (₹1200)": (
                {"cash": -1200, "insurance": True, "confidence": +4}
                if p["cash"] >= 1200 else
                {"stress": +3, "regret": +4}
            ),
            "Ignore it": {"regret": +3}
        }
    }

def phone_damage_event(p):
    if p["insurance"]:
        return {
            "story": "Your phone breaks, but insurance covers it.",
            "auto": {"stress": -4, "confidence": +3}
        }
    elif p["savings"] >= 8000:
        return {
            "story": "Your phone breaks. You pay from savings.",
            "auto": {"savings": -8000, "stress": +3}
        }
    else:
        return {
            "story": "Your phone breaks. You take a loan.",
            "auto": {"loan": +8000, "stress": +8, "regret": +6}
        }

def credit_card_event(p):
    return {
        "story": "A bank offers you a student credit card.",
        "choices": {
            "Take it": {"confidence": +2},
            "Reject it": {"confidence": +1}
        }
    }
def exam_fee_event(p):
    return {
        "story": "Semester exam fees are due this week.",
        "choices": {
            "Pay from cash": {"cash": -3000, "stress": -2},
            "Use savings": {"savings": -3000, "stress": +1},
            "Borrow from friend": {"loan": +3000, "stress": +3, "regret": +2}
        }
    }

def laptop_purchase_event(p):
    return {
        "story": "You need a laptop for projects and internships.",
        "choices": {
            "Buy mid-range laptop": {"cash": -25000, "confidence": +5} if p["cash"] >= 25000 else {"stress": +4},
            "Buy second-hand": {"cash": -12000, "confidence": +2},
            "Delay purchase": {"regret": +3}
        }
    }

def freelancing_event(p):
    if p["confidence"] >= 55:
        return {
            "story": "You get your first freelancing gig!",
            "auto": {"cash": +6000, "confidence": +4}
        }
    else:
        return {
            "story": "You apply for freelancing work but get no response.",
            "auto": {"regret": +2}
        }

def party_pressure_event(p):
    return {
        "story": "Friends insist you join an expensive party weekend.",
        "choices": {
            "Go all out": {"cash": -4000, "confidence": +2, "stress": +3},
            "Set a budget": {"cash": -1500, "confidence": +3},
            "Skip it": {"confidence": +1, "regret": +1}
        }
    }

def scholarship_event(p):
    if p["confidence"] >= 60:
        return {
            "story": "You win a merit-based scholarship!",
            "auto": {"savings": +12000, "confidence": +6}
        }
    else:
        return {
            "story": "You were eligible for a scholarship but missed the deadline.",
            "auto": {"regret": +4}
        }

def emergency_trip_event(p):
    return {
        "story": "You must travel home urgently due to a family issue.",
        "choices": {
            "Book train ticket": {"cash": -1500},
            "Book last-minute flight": {"cash": -6000, "stress": -1},
            "Borrow money": {"loan": +3000, "stress": +4}
        }
    }

def phone_upgrade_event(p):
    return {
        "story": "Your friends are upgrading their phones.",
        "choices": {
            "Buy new phone": {"cash": -18000, "confidence": +2},
            "Keep current phone": {"confidence": +2},
            "Buy on EMI": {"loan": +18000, "stress": +4}
        }
    }

def stock_market_event(p):
    return {
        "story": "You hear classmates making money from stocks.",
        "choices": {
            "Invest small amount": {"cash": -3000, "investments": +3000, "confidence": +2},
            "Avoid risk": {"confidence": +1},
            "Borrow to invest": {"loan": +5000, "investments": +5000, "stress": +6}
        }
    }

def failed_investment_event(p):
    if p["investments"] > 0:
        return {
            "story": "One of your investments performs poorly.",
            "auto": {"investments": -2000, "stress": +4}
        }
    else:
        return {
            "story": "Market volatility scares you, but you had no exposure.",
            "auto": {"confidence": +1}
        }

def fest_organizer_event(p):
    return {
        "story": "You join the college fest organizing committee.",
        "choices": {
            "Take leadership role": {"confidence": +5, "stress": +4},
            "Participate casually": {"confidence": +2},
            "Avoid involvement": {"regret": +2}
        }
    }

def bank_account_event(p):
    return {
        "story": "You are encouraged to open a zero-balance bank account.",
        "choices": {
            "Open account": {"confidence": +3},
            "Ignore": {"regret": +2}
        }
    }

def internship_expense_event(p):
    return {
        "story": "Your internship requires relocation expenses.",
        "choices": {
            "Use savings": {"savings": -5000, "confidence": +3},
            "Ask parents": {"stress": +1},
            "Decline internship": {"regret": +6}
        }
    }

def exam_failure_event(p):
    if p["stress"] > 50:
        return {
            "story": "High stress affects your exam performance.",
            "auto": {"confidence": -6, "regret": +5}
        }
    else:
        return {
            "story": "You clear exams comfortably.",
            "auto": {"confidence": +3}
        }

def startup_idea_event(p):
    return {
        "story": "You have a small startup idea with friends.",
        "choices": {
            "Invest time and money": {"cash": -5000, "confidence": +5},
            "Just observe": {"confidence": +2},
            "Reject idea": {"regret": +2}
        }
    }

def placement_season_event(p):
    if p["confidence"] >= 65:
        return {
            "story": "You get placed during campus placements!",
            "auto": {"cash": +20000, "confidence": +8}
        }
    else:
        return {
            "story": "Placement season passes without an offer.",
            "auto": {"stress": +6, "regret": +6}
        }
def internship_event(p):
    if p["confidence"] >= 55:
        return {
            "story": "You crack a paid internship!",
            "auto": {"cash": +8000, "confidence": +6}
        }
    else:
        return {
            "story": "You miss an internship opportunity.",
            "auto": {"regret": +4}
        }

def medical_event(p):
    if p["insurance"]:
        return {
            "story": "You fall sick. Insurance saves you.",
            "auto": {"cash": -2000, "stress": -5}
        }
    elif p["savings"] >= 15000:
        return {
            "story": "You pay medical bills from savings.",
            "auto": {"savings": -15000, "stress": +4}
        }
    else:
        return {
            "story": "You take a loan for medical expenses.",
            "auto": {"loan": +15000, "stress": +10, "regret": +8}
        }

# ---------------- EVENT LIST ----------------
EVENTS = [
    allowance_event,
    bank_account_event,
    insurance_event,
    exam_fee_event,
    phone_damage_event,
    credit_card_event,
    laptop_purchase_event,
    party_pressure_event,
    stock_market_event,
    failed_investment_event,
    freelancing_event,
    emergency_trip_event,
    fest_organizer_event,
    internship_event,
    internship_expense_event,
    medical_event,
    scholarship_event,
    phone_upgrade_event,
    startup_idea_event,
    exam_failure_event,
    placement_season_event
]


# ---------------- UI ----------------
st.title("🎓 College Financial Life Simulator")

st.sidebar.header("📊 Your Life Stats")
st.sidebar.write(f"💵 Cash: ₹{player['cash']}")
st.sidebar.write(f"🏦 Savings: ₹{player['savings']}")
st.sidebar.write(f"📉 Loan: ₹{player['loan']}")
st.sidebar.write(f"📈 Investments: ₹{player['investments']}")
st.sidebar.write(f"🛡️ Insurance: {player['insurance']}")
st.sidebar.write(f"😌 Confidence: {player['confidence']}")
st.sidebar.write(f"😰 Stress: {player['stress']}")
st.sidebar.write(f"😔 Regret: {player['regret']}")

# ---------------- GAME LOOP ----------------
if player["event_index"] >= len(EVENTS):
    st.success("🎉 Your college life simulation continues beyond this demo.")
    st.stop()

event_fn = EVENTS[player["event_index"]]
event = event_fn(player)

st.subheader(f"Life Event {player['event_index'] + 1}")
st.write(event["story"])

# CHOICE EVENT
if "choices" in event:
    choice = st.radio("What do you do?", list(event["choices"].keys()))
    if st.button("Confirm Decision"):
        effects = event["choices"][choice]
        apply_effects(effects)
        player["history"].append(event["story"] + " → " + choice)
        player["event_index"] += 1
        st.rerun()

# AUTO CONSEQUENCE EVENT
else:
    st.info("Life happens. You had no choice here.")
    if st.button("Continue"):
        apply_effects(event["auto"])
        player["history"].append(event["story"])
        player["event_index"] += 1
        st.rerun()

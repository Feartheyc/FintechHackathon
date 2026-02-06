import streamlit as st

st.set_page_config(page_title="ArthQuest — College Student", layout="centered")

# ---------------- EVENTS (COLLEGE STUDENT) ----------------
EVENTS = [
    {
        "title": "Pocket Money Delay",
        "story": "Your parents inform you that this month's pocket money will be delayed. Hostel rent is due soon.",
        "choices": {
            "Use emergency savings": {
                "cash": -2000, "savings": -2000, "confidence": +5, "stress": -5
            },
            "Borrow from a friend": {
                "cash": +2000, "loan": +2000, "stress": +5, "regret": +3
            },
            "Delay rent payment": {
                "stress": +15, "confidence": -10, "regret": +5
            }
        }
    },
    {
        "title": "Subscription Drain",
        "story": "Multiple OTT and food app subscriptions auto-deduct ₹999 this month.",
        "choices": {
            "Cancel unused subscriptions": {
                "cash": +400, "confidence": +5
            },
            "Ignore (small amount mindset)": {
                "cash": -999, "stress": +5, "regret": +6
            },
            "Ask parents for extra money": {
                "cash": +1000, "confidence": -10
            }
        }
    },
    {
        "title": "Friends’ Trip Pressure",
        "story": "Your friends plan a weekend trip costing ₹3,500 per person.",
        "choices": {
            "Go on the trip": {
                "cash": -3500, "stress": +5
            },
            "Suggest a cheaper plan": {
                "cash": -800, "confidence": +10
            },
            "Say no": {
                "confidence": +5, "regret": +2
            }
        }
    },
    {
        "title": "Online Sale Temptation",
        "story": "A limited-time sale offers your favorite jacket. EMI option available.",
        "choices": {
            "Buy using EMI": {
                "emi": +1200, "stress": +6, "regret": +5
            },
            "Wait and save": {
                "confidence": +10
            },
            "Buy cheaper alternative": {
                "cash": -600
            }
        }
    },
    {
        "title": "Sudden Illness During Exams",
        "story": "You fall sick. Tests and medicines cost ₹2,500. No insurance.",
        "choices": {
            "Pay from savings": {
                "cash": -2500, "savings": -2500, "stress": -5
            },
            "Skip tests": {
                "cash": -500, "regret": +10, "stress": +8
            },
            "Ask parents for help": {
                "cash": +2500, "confidence": -10
            }
        }
    },
    {
        "title": "First Credit Card Offer",
        "story": "A bank offers you a student credit card with no annual fee.",
        "choices": {
            "Use only for essentials, repay fully": {
                "confidence": +10, "stress": -5
            },
            "Use freely, pay minimum due": {
                "loan": +3000, "stress": +12, "regret": +12
            },
            "Reject the offer": {
                "confidence": +4
            }
        }
    },
    {
        "title": "First Investment Exposure",
        "story": "A friend explains SIPs and long-term investing.",
        "choices": {
            "Start small SIP (₹500)": {
                "savings": -500, "confidence": +10
            },
            "Invest blindly in trending asset": {
                "cash": -2000, "regret": +8, "stress": +6
            },
            "Ignore investing": {
                "confidence": -4, "regret": +4
            }
        }
    }
]

# ---------------- STATE ----------------
def init_state():
    return {
        "level": 0,
        "cash": 6000,
        "savings": 2000,
        "loan": 0,
        "emi": 0,
        "confidence": 50,
        "stress": 25,
        "regret": 0
    }

if "player" not in st.session_state:
    st.session_state.player = init_state()

player = st.session_state.player

# ---------------- UI ----------------
st.title("🎓 ArthQuest — College Student")

st.subheader("📊 Financial Dashboard")
st.write(f"💵 Cash: ₹{player['cash']}")
st.write(f"🏦 Savings: ₹{player['savings']}")
st.write(f"📉 Loan: ₹{player['loan']}")
st.write(f"🧾 EMI: ₹{player['emi']}")

st.progress(player["confidence"] / 100)
st.caption(f"Confidence: {player['confidence']}")

st.progress(player["stress"] / 100)
st.caption(f"Stress: {player['stress']}")

st.progress(min(player["regret"], 100) / 100)
st.caption(f"Regret: {player['regret']}")

st.divider()

# ---------------- GAME LOOP ----------------
if player["level"] < len(EVENTS):
    event = EVENTS[player["level"]]

    st.subheader(f"Month {player['level'] + 1}: {event['title']}")
    st.write(event["story"])

    choice = st.radio("Your decision:", list(event["choices"].keys()))

    if st.button("Confirm Decision ➜"):
        effects = event["choices"][choice]

        for k, v in effects.items():
            player[k] += v

        # clamps
        player["confidence"] = max(0, min(100, player["confidence"]))
        player["stress"] = max(0, min(100, player["stress"]))
        player["cash"] = max(0, player["cash"])

        player["level"] += 1
        st.rerun()

else:
    # ---------------- ENDING ----------------
    st.subheader("🏁 Year End Outcome")

    final_score = (
        player["confidence"]
        - player["stress"]
        - player["regret"]
        - int(player["loan"] * 0.01)
    )

    st.write(f"### Final Financial Score: **{final_score}**")

    if final_score >= 60:
        st.success("🌟 Financially confident and future-ready.")
    elif final_score >= 30:
        st.warning("⚠️ Managing, but vulnerable to shocks.")
    else:
        st.error("❌ High stress and poor financial resilience.")

    if st.button("🔁 Restart Game"):
        st.session_state.player = init_state()
        st.rerun()

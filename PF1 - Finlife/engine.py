import streamlit as st

def init_game(persona):
    defaults = {
        "Student": {"cash": 6000, "savings": 2000, "loan": 0, "investments": 0, "stress": 25},
        "Farmer": {"cash": 10000, "savings": 5000, "loan": 0, "investments": 500000, "stress": 10},
        "Employee": {"cash": 50000, "savings": 100000, "loan": 0, "investments": 50000, "stress": 40},
        "Founder": {"cash": 200000, "savings": 20000, "loan": 0, "investments": 0, "stress": 60}
    }
    base = defaults.get(persona, defaults["Student"])
    return {
        "state": "MAP", 
        "persona": persona, "event_index": 0,
        "cash": base['cash'], "savings": base['savings'], "loan": base['loan'],
        "investments": base['investments'], "insurance": False,
        "confidence": 50, "stress": base['stress'], "regret": 0,
        "history": [], "last_feedback": None, "feedback_type": "info", "flags": {}
    }

def try_apply_effects(effects):
    p = st.session_state.game
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
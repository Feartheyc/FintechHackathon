import streamlit as st

def c(text, effects, msg=None):
    return {"text": text, "effects": effects, "msg": msg}

# --- ADD THIS GLOSSARY SECTION ---
GLOSSARY = {
    "KCC": "Kisan Credit Card: Low interest loans for farmers.",
    "Hybrid": "High-yield seeds that need more water.",
    "Mandi": "Wholesale market for crops.",
    "Interest": "Extra money paid back on a loan.",
    "Subsidy": "Government discount.",
    "Asset": "Valuable item owned (land, gold).",
    "PF": "Provident Fund: Retirement savings.",
    "EMI": "Monthly loan repayment.",
    "SIP": "Systematic Investment: Monthly investing.",
    "Inflation": "Price rise over time.",
    "Equity": "Ownership share in a business.",
    "Bootstrap": "Starting business with own money.",
    "VC": "Investors who fund startups.",
    "Burn Rate": "Monthly cash spending speed.",
    "Runway": "Months left before money runs out.",
    "Pivot": "Changing business strategy.",
    "IPO": "Selling shares to public market."
}
# ---------------------------------

STATIC_CAMPAIGNS = {
    "Farmer": {
        0: { "title": "Sowing Season", "npc": "Moneylender Seth", "avatar": "👹", "text": "Ramesh! Why run to the bank? Take ₹20,000 cash now. No paperwork.", "thought": "Bank takes days... but Seth's interest is deadly. The rain is coming soon.", "choices": [c("Take Seth's Cash", {"cash": 20000, "loan": 20000, "add_flag": "predatory_loan"}, "Debt Trap: 50% Interest rate!"), c("Go to Bank (KCC)", {"cash": 20000, "loan": 20000, "confidence": 10}, "Safe Loan: 7% Interest.")] },
        1: { "title": "Seed Quality", "npc": "Shopkeeper", "avatar": "🏪", "text": "I have Hybrid Seeds (₹3,000) and Local Seeds (₹1,000). Hybrid gives double yield but needs water.", "thought": "My borewell is old... if the rains fail, hybrid crops will die.", "choices": [c("Buy Hybrid", {"cash": -3000, "add_flag": "hybrid_seeds"}, "High Potential."), c("Buy Local", {"cash": -1000}, "Low Cost.")] },
        2: { "title": "Harvest Price", "npc": "Middleman", "avatar": "⚖️", "text": "Price is ₹10/kg here. Mandi is 50km away, but prices are better there.", "thought": "I'm tired from the harvest. Going to Mandi means renting a truck.", "choices": [c("Sell Here", {"cash": 30000, "regret": 10}, "Quick cash."), c("Go to Mandi", {"cash": 45000, "stress": 5}, "Hard work pays off.")] },
        3: { "title": "Loan Repayment", "npc": "Bank Manager", "avatar": "🏦", "text": "Namaste Ramesh. Your crop loan is due. Can you clear it today?", "thought": "I have the cash, but what if an emergency comes up?", "choices": [c("Repay Full", {"cash": -20000, "loan": -20000, "confidence": 10}, "Debt Free."), c("Delay", {"stress": 10, "loan": 2000}, "Interest piling up.")] },
        4: { "title": "Daughter's School", "npc": "Wife", "avatar": "👩", "text": "Lakshmi needs admission. The Private school is ₹15k, but the Govt school is free.", "thought": "I want her to have the life I never had.", "choices": [c("Private School", {"cash": -15000, "success": 20}, "Better future."), c("Govt School", {"success": 5}, "Saved money.")] },
        5: { "title": "Tractor", "npc": "Dealer", "avatar": "🚜", "text": "Why use bullocks? Buy a Tractor! I'll arrange a ₹5 Lakh loan instantly.", "thought": "A tractor would make me a king in the village... but the debt?", "choices": [c("Buy Tractor", {"loan": 500000, "stress": 20}, "Status symbol."), c("Rent when needed", {"cash": -5000}, "Smart choice.")] },
        6: { "title": "Sister's Wedding", "npc": "Family", "avatar": "🎉", "text": "The wedding must be grand! We need ₹2 Lakhs for the feast.", "thought": "If I don't spend, the village will talk. If I do, I lose my land.", "choices": [c("Sell Land", {"cash": 500000, "add_flag": "sold_land", "regret": 20}, "Asset lost."), c("Simple Wedding", {"cash": -50000}, "Social pressure ignored.")] },
    },
    "Employee": {
        0: { "title": "Job Offer", "npc": "HR", "avatar": "👔", "text": "Welcome aboard! We can structure your salary: High Cash in hand or Higher PF contribution?", "thought": "Cash buys things today. PF buys freedom later.", "choices": [c("High Cash", {"cash": 50000}, "Instant gratification."), c("High PF", {"cash": 40000, "savings": 10000}, "Retirement secured.")] },
        1: { "title": "New Phone", "npc": "Advertisement", "avatar": "📱", "text": "Flash Sale! The iPhone 16 Pro Max is finally here. EMI starts at ₹5000!", "thought": "My current phone works fine, but everyone at the office has the new one...", "choices": [c("Buy on EMI", {"loan": 80000, "regret": 10}, "Costly status."), c("Keep Old Phone", {"savings": 5000}, "Saved money.")] },
        2: { "title": "Car Purchase", "npc": "Family", "avatar": "🚗", "text": "Everyone else has a new car. We should get an SUV!", "thought": "An SUV is a status symbol, but a hatchback is debt-free.", "choices": [c("New SUV", {"loan": 1500000, "stress": 10}, "Big EMI."), c("Used Hatchback", {"cash": -200000}, "Debt free.")] },
        3: { "title": "Stock Tip", "npc": "Friend", "avatar": "📉", "text": "Bro, I heard this penny stock is going to double in 2 days. Invest now!", "thought": "Get rich quick schemes usually end badly... but what if he's right?", "choices": [c("Gamble", {"cash": -50000, "regret": 20}, "Lost everything."), c("Stick to SIP", {"investments": 20000}, "Disciplined.")] },
        4: { "title": "Medical Insurance", "npc": "Insurance Agent", "avatar": "🏥", "text": "Sir, one medical emergency can wipe your savings. Cover parents for just ₹25k?", "thought": "I'm young and healthy. Do I really need this expense?", "choices": [c("Buy Policy", {"cash": -25000, "insurance": True}, "Safety net."), c("Skip", {}, "Huge risk.")] },
        5: { "title": "Home Renovation", "npc": "Contractor", "avatar": "🔨", "text": "The kitchen looks old. Let's redo it completely for ₹3 Lakhs.", "thought": "It would look great, but I'd have to take a personal loan.", "choices": [c("Personal Loan", {"loan": 300000}, "High interest."), c("Delay", {"stress": 5}, "Save first.")] },
        6: { "title": "Layoff Rumors", "npc": "Colleague", "avatar": "🏢", "text": "Did you hear? They might fire 20% of the staff next month.", "thought": "Panic won't help. I should probably save cash and upskill.", "choices": [c("Up-skill Course", {"cash": -5000, "confidence": 10}, "Safe."), c("Ignore", {"stress": 20}, "Risky.")] },
    },
    "Founder": {
        0: { "title": "The Idea", "npc": "Inner Voice", "avatar": "💡", "text": "You have a unicorn idea. Quit your job to pursue it?", "thought": "High risk, infinite reward.", "choices": [c("Quit Job", {"cash": -20000, "stress": 10, "confidence": 10}, "All In."), c("Side Hustle", {"stress": 20}, "Safe play.")]},
        1: { "title": "Co-Founder", "npc": "Tech Whiz", "avatar": "🧑‍💻", "text": "I can build the tech, but I want 50% equity.", "thought": "He's a genius but expensive.", "choices": [c("Agree", {"confidence": 10}, "Strong Team."), c("Hire Freelancer", {"cash": -30000}, "Kept Equity.")]},
        2: { "title": "MVP Launch", "npc": "Market", "avatar": "🚀", "text": "Product is buggy. Launch anyway?", "thought": "Speed is life.", "choices": [c("Launch Now", {"cash": 10000, "stress": 10}, "Feedback"), c("Perfect It", {"cash": -20000}, "Burn Rate Up")]},
        3: { "title": "Seed Round", "npc": "VC", "avatar": "💰", "text": "We offer ₹1 Crore for 20% equity.", "thought": "Fuel for the rocket ship.", "choices": [c("Take Money", {"cash": 10000000, "stress": -10}, "Funded!"), c("Bootstrap", {"confidence": 20, "stress": 20}, "Freedom.")]},
        4: { "title": "The Pivot", "npc": "Analytics", "avatar": "📊", "text": "Users hate feature A but love feature B. Pivot?", "thought": "Changing direction is costly.", "choices": [c("Pivot", {"cash": -50000, "confidence": 10}, "Adapt."), c("Stay Course", {"stress": 10}, "Stubborn.")]},
        5: { "title": "Cash Crunch", "npc": "CFO", "avatar": "📉", "text": "2 months of runway left.", "thought": "Do or die.", "choices": [c("Fire Sales Team", {"stress": 20, "regret": 10}, "Lean Ops."), c("Founder Salary Cut", {"confidence": 5}, "Lead by example.")]},
        6: { "title": "The Exit", "npc": "Big Tech", "avatar": "🏢", "text": "Acquisition offer: ₹50 Crores.", "thought": "Generational wealth?", "choices": [c("Sell", {"cash": 50000000}, "Exit Strategy."), c("IPO", {"confidence": 30, "stress": 30}, "Legacy.")]}
    }
}

def stud_allowance(p): return {"story": "Here is your monthly allowance, son. Try to make it last the whole month, okay?", "npc": "Dad", "avatar": "👨‍🦳", "thought": "It's barely enough... I need to budget this carefully.", "choices": {"Save most": {"cash": +1000, "savings": +3000, "confidence": +3}, "Spend freely": {"cash": -4000, "confidence": +2, "stress": +2}, "Split wisely": {"cash": +2500, "savings": +1500}}}
def stud_insurance(p): return {"story": "Listen kid, I broke my leg playing football and the bill was huge. You really should get that student health insurance.", "npc": "Senior Student", "avatar": "🎓", "thought": "₹1200 is a lot of pizza money... but an accident would ruin me.", "choices": {"Buy insurance": ({"cash": -1200, "insurance": True, "confidence": +4} if p["cash"] >= 1200 else {"stress": +3}), "Ignore advice": {"regret": +3}}}
def stud_exam(p): return {"story": "This is the final notice. Semester exam fees of ₹3000 are due immediately.", "npc": "Admin Office", "avatar": "🏫", "thought": "I totally forgot! Where do I get the money now?", "choices": {"Pay from Cash": {"cash": -3000, "stress": -2}, "Pay from Savings": {"savings": -3000, "stress": +1}, "Borrow": {"loan": +3000, "stress": +3}}}
def stud_phone(p):
    if p["insurance"]: return {"story": "Ouch! Your screen is shattered. But wait... you have insurance! We'll fix this for free.", "npc": "Repair Shop", "avatar": "🛠️", "thought": "Thank god I listened to that senior!", "auto": {"stress": -4, "insurance": False}}
    return {"story": "Ouch! Your screen is shattered. Replacing this display is going to cost you ₹8,000.", "npc": "Repair Shop", "avatar": "🛠️", "thought": "This is a disaster. I don't have that kind of cash lying around.", "choices": {"Pay Cash": {"cash": -8000, "stress": +5}, "Take Loan": {"loan": 8000, "stress": +10}}}
def stud_crypto(p): return {"story": "Bro! Trust me, 'DogeMoon' is going to the moon! Put in ₹2,000 now and you'll be rich next week!", "npc": "Roommate", "avatar": "😎", "thought": "He sounds convincing... but this sounds like a scam.", "choices": {"Invest ₹2000": {"cash": -2000, "regret": 5}, "Refuse": {"confidence": 5}}}
def stud_intern(p):
    if p['confidence'] > 50: return {"story": "We were really impressed by your confidence during the interview. We'd like to offer you a paid internship!", "npc": "Recruiter", "avatar": "🤝", "thought": "Yes! All that hard work paid off!", "auto": {"cash": 10000, "confidence": 10}}
    return {"story": "You have good grades, but you seemed very unsure of yourself. We're going with another candidate.", "npc": "Recruiter", "avatar": "🤝", "thought": "I choked... I need to work on my confidence.", "auto": {"stress": 10}}

STUDENT_EVENTS = [stud_allowance, stud_insurance, stud_crypto, stud_exam, stud_phone, stud_intern]

def get_event_data(persona, index):
    if persona == "Student":
        if index < len(STUDENT_EVENTS): return STUDENT_EVENTS[index](st.session_state.game)
        return None
    if persona in STATIC_CAMPAIGNS:
        campaign = STATIC_CAMPAIGNS[persona]
        if index in campaign:
            raw = campaign[index]
            choices_dict = {}
            for c_item in raw['choices']:
                effect = c_item['effects'].copy()
                effect['__msg'] = c_item['msg'] 
                choices_dict[c_item['text']] = effect
            return {"story": raw['text'], "choices": choices_dict, "npc": raw['npc'], "avatar": raw['avatar'], "thought": raw.get('thought', "...")}
    return None
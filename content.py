import streamlit as st

def c(text, effects, msg=None):
    return {"text": text, "effects": effects, "msg": msg}

# --- GLOSSARY ---
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
    "IPO": "Selling shares to public market.",
    "ELSS": "Tax-saving mutual funds with a 3-year lock-in.",
    "Organic": "Farming without chemicals, crops sell for higher prices.",
    "Solar Pump": "Water pump running on sun energy, saves electricity bill.",
    "Freelance": "Working part-time for different clients to earn extra money."
}

STATIC_CAMPAIGNS = {
    "Farmer": {
        0: { 
            "title": "Sowing Season", "npc": "Moneylender Seth", "avatar": "👹", 
            "text": "Ramesh! Why run to the bank? Take ₹20,000 cash now. No paperwork.", 
            "thought": "Bank takes days... but Seth's interest is deadly. The rain is coming soon.", 
            "advisor": "Avoid informal loans (Moneylenders) at all costs. They charge 50%+ interest. The Bank (KCC) charges only 7%. A small delay is better than a debt trap.",
            "choices": [c("Take Seth's Cash", {"cash": 20000, "loan": 20000, "add_flag": "predatory_loan"}, "Debt Trap: 50% Interest rate!"), c("Go to Bank (KCC)", {"cash": 20000, "loan": 20000, "confidence": 10}, "Safe Loan: 7% Interest.")] 
        },
        1: { 
            "title": "Seed Quality", "npc": "Shopkeeper", "avatar": "🏪", 
            "text": "I have Hybrid Seeds (₹3,000) and Local Seeds (₹1,000). Hybrid gives double yield but needs water.", 
            "thought": "My borewell is old... if the rains fail, hybrid crops will die.", 
            "advisor": "High risk can mean high reward, but only if you have the infrastructure (water). Since your borewell is old, Hybrid seeds are a gamble. Local seeds are safer for your current situation.",
            "choices": [c("Buy Hybrid", {"cash": -3000, "add_flag": "hybrid_seeds"}, "High Potential."), c("Buy Local", {"cash": -1000}, "Low Cost.")] 
        },
        2: { 
            "title": "Harvest Price", "npc": "Middleman", "avatar": "⚖️", 
            "text": "Price is ₹10/kg here. Mandi is 50km away, but prices are better there.", 
            "thought": "I'm tired from the harvest. Going to Mandi means renting a truck.", 
            "advisor": "Middlemen often underpay. Even with transport costs, the Mandi usually offers fair market value. Don't let laziness eat your profits.",
            "choices": [c("Sell Here", {"cash": 30000, "regret": 10}, "Quick cash."), c("Go to Mandi", {"cash": 45000, "stress": 5}, "Hard work pays off.")] 
        },
        3: { 
            "title": "Loan Repayment", "npc": "Bank Manager", "avatar": "🏦", 
            "text": "Namaste Ramesh. Your crop loan is due. Can you clear it today?", 
            "thought": "I have the cash, but what if an emergency comes up?", 
            "advisor": "Always prioritize clearing debt when you have cash. Interest compounds over time. Being debt-free reduces stress and improves credit scores for future loans.",
            "choices": [c("Repay Full", {"cash": -20000, "loan": -20000, "confidence": 10}, "Debt Free."), c("Delay", {"stress": 10, "loan": 2000}, "Interest piling up.")] 
        },
        4: { 
            "title": "Daughter's School", "npc": "Wife", "avatar": "👩", 
            "text": "Lakshmi needs admission. The Private school is ₹15k, but the Govt school is free.", 
            "thought": "I want her to have the life I never had.", 
            "advisor": "Education is an investment, not an expense. If you can afford it without taking a high-interest loan, quality education yields the highest returns in the long run.",
            "choices": [c("Private School", {"cash": -15000, "success": 20}, "Better future."), c("Govt School", {"success": 5}, "Saved money.")] 
        },
        5: { 
            "title": "Tractor", "npc": "Dealer", "avatar": "🚜", 
            "text": "Why use bullocks? Buy a Tractor! I'll arrange a ₹5 Lakh loan instantly.", 
            "thought": "A tractor would make me a king in the village... but the debt?", 
            "advisor": "Don't buy depreciating assets (machines that lose value) on huge debt unless you have a massive farm. Renting is financially smarter for small farmers.",
            "choices": [c("Buy Tractor", {"loan": 500000, "stress": 20}, "Status symbol."), c("Rent when needed", {"cash": -5000}, "Smart choice.")] 
        },
        6: { 
            "title": "Sister's Wedding", "npc": "Family", "avatar": "🎉", 
            "text": "The wedding must be grand! We need ₹2 Lakhs for the feast.", 
            "thought": "If I don't spend, the village will talk. If I do, I lose my land.", 
            "advisor": "Selling productive assets (Land) for consumption (Wedding) is a classic poverty trap. Ignore social pressure. Preserve your wealth-generating assets.",
            "choices": [c("Sell Land", {"cash": 500000, "add_flag": "sold_land", "regret": 20}, "Asset lost."), c("Simple Wedding", {"cash": -50000}, "Social pressure ignored.")] 
        },
        7: { 
            "title": "Solar Upgrade", "npc": "Govt Officer", "avatar": "👮", 
            "text": "Install a Solar Pump for ₹50,000? Govt gives 40% subsidy.", 
            "thought": "It saves diesel money forever, but the upfront cost is high.", 
            "advisor": "With a 40% subsidy, the Solar Pump pays for itself in diesel savings within 2 years. This is a high-return capital investment.",
            "choices": [c("Install Solar", {"cash": -30000, "confidence": 15}, "Free Electricity!"), c("Stick to Diesel", {"cash": -2000}, "High Running Cost.")] 
        },
        8: { 
            "title": "Organic Farming", "npc": "NGO Worker", "avatar": "🌱", 
            "text": "Switch to Organic farming? You'll get double prices next year.", 
            "thought": "Yield will be low this year... can I survive the dip?", 
            "advisor": "Organic is the future, but the transition period is tough. Only switch if you have enough savings to survive 1-2 years of lower yields.",
            "choices": [c("Go Organic", {"cash": -5000, "confidence": 20, "stress": 10}, "Future Ready."), c("Chemical Farming", {"cash": 5000}, "Immediate Yield.")] 
        },
    },
    "Employee": {
        0: { 
            "title": "Job Offer", "npc": "HR", "avatar": "👔", 
            "text": "Welcome aboard! We can structure your salary: High Cash in hand or Higher PF contribution?", 
            "thought": "Cash buys things today. PF buys freedom later.", 
            "advisor": "PF (Provident Fund) is forced savings with compound interest. It's the safest way to build a retirement corpus. Sacrifice a little cash today for a secure tomorrow.",
            "choices": [c("High Cash", {"cash": 50000}, "Instant gratification."), c("High PF", {"cash": 40000, "savings": 10000}, "Retirement secured.")] 
        },
        1: { 
            "title": "New Phone", "npc": "Advertisement", "avatar": "📱", 
            "text": "Flash Sale! The iPhone 16 Pro Max is finally here. EMI starts at ₹5000!", 
            "thought": "My current phone works fine, but everyone at the office has the new one...", 
            "advisor": "Never take a loan (EMI) for a depreciating asset like a phone. Its value drops the moment you buy it. Stick to the old phone and invest that EMI amount instead.",
            "choices": [c("Buy on EMI", {"loan": 80000, "regret": 10}, "Costly status."), c("Keep Old Phone", {"savings": 5000}, "Saved money.")] 
        },
        2: { 
            "title": "Car Purchase", "npc": "Family", "avatar": "🚗", 
            "text": "Everyone else has a new car. We should get an SUV!", 
            "thought": "An SUV is a status symbol, but a hatchback is debt-free.", 
            "advisor": "A car is not an asset; it's a liability that drinks fuel and loses value. A used hatchback offers 90% of the utility for 20% of the price. Stay debt-free.",
            "choices": [c("New SUV", {"loan": 1500000, "stress": 10}, "Big EMI."), c("Used Hatchback", {"cash": -200000}, "Debt free.")] 
        },
        3: { 
            "title": "Stock Tip", "npc": "Friend", "avatar": "📉", 
            "text": "Bro, I heard this penny stock is going to double in 2 days. Invest now!", 
            "thought": "Get rich quick schemes usually end badly... but what if he's right?", 
            "advisor": "Penny stocks are often scams or gambling. Systematic Investment Plans (SIP) in index funds create wealth over time. Don't gamble; invest.",
            "choices": [c("Gamble", {"cash": -50000, "regret": 20}, "Lost everything."), c("Stick to SIP", {"investments": 20000}, "Disciplined.")] 
        },
        4: { 
            "title": "Medical Insurance", "npc": "Insurance Agent", "avatar": "🏥", 
            "text": "Sir, one medical emergency can wipe your savings. Cover parents for just ₹25k?", 
            "thought": "I'm young and healthy. Do I really need this expense?", 
            "advisor": "Insurance is not an expense; it's wealth protection. One hospital bill can cost ₹5 Lakhs. Paying ₹25k now prevents bankruptcy later.",
            "choices": [c("Buy Policy", {"cash": -25000, "insurance": True}, "Safety net."), c("Skip", {}, "Huge risk.")] 
        },
        5: { 
            "title": "Home Renovation", "npc": "Contractor", "avatar": "🔨", 
            "text": "The kitchen looks old. Let's redo it completely for ₹3 Lakhs.", 
            "thought": "It would look great, but I'd have to take a personal loan.", 
            "advisor": "Personal loans have very high interest (12-18%). Save up for the renovation first. Never borrow for cosmetic upgrades.",
            "choices": [c("Personal Loan", {"loan": 300000}, "High interest."), c("Delay", {"stress": 5}, "Save first.")] 
        },
        6: { 
            "title": "Layoff Rumors", "npc": "Colleague", "avatar": "🏢", 
            "text": "Did you hear? They might fire 20% of the staff next month.", 
            "thought": "Panic won't help. I should probably save cash and upskill.", 
            "advisor": "In uncertain times, 'Cash is King'. Hoard liquidity and invest in your skills. This makes you indispensable or ready for a new job.",
            "choices": [c("Up-skill Course", {"cash": -5000, "confidence": 10}, "Safe."), c("Ignore", {"stress": 20}, "Risky.")] 
        },
        7: { 
            "title": "Tax Season", "npc": "Accountant", "avatar": "📑", 
            "text": "You owe ₹30,000 in tax. Invest in ELSS funds to save it?", 
            "thought": "ELSS locks money for 3 years, but I save tax now.", 
            "advisor": "ELSS gives you two benefits: Tax saving (Section 80C) + Wealth creation via Equity. It's a no-brainer compared to just paying tax to the govt.",
            "choices": [c("Invest in ELSS", {"cash": -30000, "investments": 30000}, "Tax Saved & Invested."), c("Pay Tax", {"cash": -30000}, "Money Gone.")] 
        },
        8: { 
            "title": "Promotion", "npc": "Boss", "avatar": "💼", 
            "text": "We are promoting you to Manager! Salary +30%, but double the stress.", 
            "thought": "More money is good, but can I handle the pressure?", 
            "advisor": "Health is wealth. If the stress leads to burnout or medical bills, the 30% hike isn't worth it. Assess your mental capacity first.",
            "choices": [c("Accept Role", {"cash": 20000, "stress": 20}, "High Earner."), c("Decline", {"stress": -10}, "Work-Life Balance.")] 
        },
    },
    "Founder": {
        0: { 
            "title": "The Idea", "npc": "Inner Voice", "avatar": "💡", 
            "text": "You have a unicorn idea. Quit your job to pursue it?", 
            "thought": "High risk, infinite reward.", 
            "advisor": "Entrepreneurship is a marathon. Ensure you have 6-12 months of emergency savings before quitting your job, or start it as a side hustle first.",
            "choices": [c("Quit Job", {"cash": -20000, "stress": 10, "confidence": 10}, "All In."), c("Side Hustle", {"stress": 20}, "Safe play.")]
        },
        1: { 
            "title": "Co-Founder", "npc": "Tech Whiz", "avatar": "🧑‍💻", 
            "text": "I can build the tech, but I want 50% equity.", 
            "thought": "He's a genius but expensive.", 
            "advisor": "Idea is cheap, execution is everything. A brilliant tech co-founder is worth 50%. 100% of nothing is nothing; 50% of a unicorn is billions.",
            "choices": [c("Agree", {"confidence": 10}, "Strong Team."), c("Hire Freelancer", {"cash": -30000}, "Kept Equity.")]
        },
        2: { 
            "title": "MVP Launch", "npc": "Market", "avatar": "🚀", 
            "text": "Product is buggy. Launch anyway?", 
            "thought": "Speed is life.", 
            "advisor": "Perfection is the enemy of progress. Launch early, get feedback, and iterate. 'Burn rate' eats your cash while you wait for perfection.",
            "choices": [c("Launch Now", {"cash": 10000, "stress": 10}, "Feedback"), c("Perfect It", {"cash": -20000}, "Burn Rate Up")]
        },
        3: { 
            "title": "Seed Round", "npc": "VC", "avatar": "💰", 
            "text": "We offer ₹1 Crore for 20% equity.", 
            "thought": "Fuel for the rocket ship.", 
            "advisor": "Taking VC money accelerates growth but adds pressure. If you can grow without it (Bootstrap), you keep control. If you need speed, take the cash.",
            "choices": [c("Take Money", {"cash": 10000000, "stress": -10}, "Funded!"), c("Bootstrap", {"confidence": 20, "stress": 20}, "Freedom.")]
        },
        4: { 
            "title": "The Pivot", "npc": "Analytics", "avatar": "📊", 
            "text": "Users hate feature A but love feature B. Pivot?", 
            "thought": "Changing direction is costly.", 
            "advisor": "Listen to the market, not your ego. If the data says pivot, pivot immediately. Persistence in the wrong direction is just failure.",
            "choices": [c("Pivot", {"cash": -50000, "confidence": 10}, "Adapt."), c("Stay Course", {"stress": 10}, "Stubborn.")]
        },
        5: { 
            "title": "Cash Crunch", "npc": "CFO", "avatar": "📉", 
            "text": "2 months of runway left.", 
            "thought": "Do or die.", 
            "advisor": "Survival is the only metric that matters now. Cut costs ruthlessly (even painful ones) to extend your runway. You can't win if you're dead.",
            "choices": [c("Fire Sales Team", {"stress": 20, "regret": 10}, "Lean Ops."), c("Founder Salary Cut", {"confidence": 5}, "Lead by example.")]
        },
        6: { 
            "title": "The Exit", "npc": "Big Tech", "avatar": "🏢", 
            "text": "Acquisition offer: ₹50 Crores.", 
            "thought": "Generational wealth?", 
            "advisor": "A bird in the hand is worth two in the bush. ₹50 Crores is life-changing. Only IPO if you want to build a legacy and can handle public market stress.",
            "choices": [c("Sell", {"cash": 50000000}, "Exit Strategy."), c("IPO", {"confidence": 30, "stress": 30}, "Legacy.")]
        },
        7: { 
            "title": "Global Expansion", "npc": "Advisor", "avatar": "🌍", 
            "text": "Expand to USA? It costs ₹2 Crores.", 
            "thought": "High risk, but we could become a global brand.", 
            "advisor": "Premature scaling is the #1 killer of startups. Expand only if your local unit economics are profitable and stable.",
            "choices": [c("Expand", {"cash": -20000000, "confidence": 20}, "Global Player."), c("Stay Local", {"cash": 5000000}, "Steady Profits.")] 
        },
        8: { 
            "title": "Market Crash", "npc": "News", "avatar": "📉", 
            "text": "Global recession hits! Revenue down 40%.", 
            "thought": "Panic selling or hold tight?", 
            "advisor": "Recessions act as a filter. If you have cash reserves, hold tight or even buy distressed assets. Panic selling locks in losses.",
            "choices": [c("Hold & Build", {"stress": 20, "investments": 5000000}, "Long Term Vision."), c("Sell Assets", {"cash": 10000000, "regret": 20}, "Safe Cash.")] 
        },
    }
}

# --- DYNAMIC PYTHON LOGIC CONTENT (STUDENT) ---
def stud_allowance(p): 
    return {
        "story": "Here is your monthly allowance, son. Try to make it last the whole month, okay?", 
        "npc": "Dad", "avatar": "👨‍🦳", 
        "thought": "It's barely enough... I need to budget this carefully.", 
        "advisor": "The 50-30-20 rule helps here. Needs (50%), Wants (30%), Savings (20%). Start saving small amounts early to build a habit.",
        "choices": {"Save most": {"cash": +1000, "savings": +3000, "confidence": +3}, "Spend freely": {"cash": -4000, "confidence": +2, "stress": +2}, "Split wisely": {"cash": +2500, "savings": +1500}}
    }

def stud_insurance(p): 
    return {
        "story": "Listen kid, I broke my leg playing football and the bill was huge. You really should get that student health insurance.", 
        "npc": "Senior Student", "avatar": "🎓", 
        "thought": "₹1200 is a lot of pizza money... but an accident would ruin me.", 
        "advisor": "You are transferring a huge financial risk (lakhs) for a small premium (hundreds). Always insure against risks you cannot afford to pay out of pocket.",
        "choices": {"Buy insurance": ({"cash": -1200, "insurance": True, "confidence": +4} if p["cash"] >= 1200 else {"stress": +3}), "Ignore advice": {"regret": +3}}
    }

def stud_exam(p): 
    return {
        "story": "This is the final notice. Semester exam fees of ₹3000 are due immediately.", 
        "npc": "Admin Office", "avatar": "🏫", 
        "thought": "I totally forgot! Where do I get the money now?", 
        "advisor": "This is why an 'Emergency Fund' is vital. Using savings is better than borrowing. Borrowing creates stress and interest obligations.",
        "choices": {"Pay from Cash": {"cash": -3000, "stress": -2}, "Pay from Savings": {"savings": -3000, "stress": +1}, "Borrow": {"loan": +3000, "stress": +3}}
    }

def stud_phone(p):
    if p["insurance"]: 
        return {
            "story": "Ouch! Your screen is shattered. But wait... you have insurance! We'll fix this for free.", 
            "npc": "Repair Shop", "avatar": "🛠️", 
            "thought": "Thank god I listened to that senior!", 
            "advisor": "See? Insurance just saved you ₹8,000. Smart financial planning pays off when things go wrong.",
            "auto": {"stress": -4, "insurance": False}
        }
    return {
        "story": "Ouch! Your screen is shattered. Replacing this display is going to cost you ₹8,000.", 
        "npc": "Repair Shop", "avatar": "🛠️", 
        "thought": "This is a disaster. I don't have that kind of cash lying around.", 
        "advisor": "If you don't have the cash, avoid high-interest loans. Try to find a cheaper repair or use a spare phone until you save up.",
        "choices": {"Pay Cash": {"cash": -8000, "stress": +5}, "Take Loan": {"loan": 8000, "stress": +10}}
    }

def stud_crypto(p): 
    return {
        "story": "Bro! Trust me, 'DogeMoon' is going to the moon! Put in ₹2,000 now and you'll be rich next week!", 
        "npc": "Roommate", "avatar": "😎", 
        "thought": "He sounds convincing... but this sounds like a scam.", 
        "advisor": "If it sounds too good to be true, it is. Never invest money you can't afford to lose in volatile assets like Crypto. Stick to safe investments.",
        "choices": {"Invest ₹2000": {"cash": -2000, "regret": 5}, "Refuse": {"confidence": 5}}
    }

def stud_intern(p):
    if p['confidence'] > 50: 
        return {
            "story": "We were really impressed by your confidence during the interview. We'd like to offer you a paid internship!", 
            "npc": "Recruiter", "avatar": "🤝", 
            "thought": "Yes! All that hard work paid off!", 
            "advisor": "Great job! Confidence comes from competence. Use this income to start your investing journey.",
            "auto": {"cash": 10000, "confidence": 10}
        }
    return {
        "story": "You have good grades, but you seemed very unsure of yourself. We're going with another candidate.", 
        "npc": "Recruiter", "avatar": "🤝", 
        "thought": "I choked... I need to work on my confidence.", 
        "advisor": "Skills get you the interview; confidence gets you the job. Invest time in soft skills training—it has a high ROI.",
        "auto": {"stress": 10}
    }

def stud_gig(p):
    return {
        "story": "I found a freelance gig online. It pays well, but I have exams next week.",
        "npc": "Laptop", "avatar": "💻", 
        "thought": "Money or Grades?", 
        "advisor": "Short-term gain (gig money) shouldn't cost you long-term value (GPA/Degree). Education is your primary job right now.",
        "choices": {"Do Gig": {"cash": 5000, "stress": 10}, "Study": {"confidence": 10}}
    }

def stud_placement(p):
    return {
        "story": "Placement interviews are starting. You need a formal suit.",
        "npc": "Warden", "avatar": "👔", 
        "thought": "A good suit costs ₹3000. It might help my impression.", 
        "advisor": "Dress for the job you want. A suit is an investment in your career. If funds are tight, borrowing or renting is acceptable for high-stakes events.",
        "choices": {"Buy Suit": {"cash": -3000, "confidence": 15}, "Borrow One": {"stress": 5}, "Go Casual": {"confidence": -10}}
    }

STUDENT_EVENTS = [stud_allowance, stud_insurance, stud_crypto, stud_exam, stud_phone, stud_intern, stud_gig, stud_placement]

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
            # ADDED: 'advisor' key to the return
            return {
                "story": raw['text'], 
                "choices": choices_dict, 
                "npc": raw['npc'], 
                "avatar": raw['avatar'], 
                "thought": raw.get('thought', "..."),
                "advisor": raw.get('advisor', "Consider your long-term goals before deciding.")
            }
    return None
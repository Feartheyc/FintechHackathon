import sqlite3
import streamlit as st

DB_FILE = "leaderboard.db"

# --- HELPER FUNCTIONS (Must be defined before they are called) ---

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            net_worth INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_score(username: str, net_worth: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO leaderboard (username, net_worth) VALUES (?, ?)", (username, net_worth))
    conn.commit()
    conn.close()

def get_leaderboard(limit: int = 10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username, net_worth FROM leaderboard ORDER BY net_worth DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

# --- MAIN UI FUNCTION ---

def render_leaderboard_ui(final_score: int = None, stats: dict = None):
    # This now works because init_db is defined above in the same file
    init_db() 
    
    st.markdown("""
        <style>
        .stats-container {
            background-color: #0e1117;
            border: 1px solid #2d2e3a;
            border-radius: 10px;
            padding: 15px;
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }
        .stat-box { text-align: center; flex: 1; border-right: 1px solid #2d2e3a; }
        .stat-box:last-child { border-right: none; }
        .stat-label { font-size: 0.7rem; color: #888; text-transform: uppercase; }
        .stat-value { font-size: 1.2rem; font-weight: bold; font-family: monospace; }
        .green { color: #4ade80; }
        .red { color: #f87171; }
        .purple { color: #c084fc; }
        </style>
    """, unsafe_allow_html=True)

    if stats is None:
        stats = {"role": "Employee", "cash": 0, "savings": 0, "debt": 0, "invest": 0, "stress": "0%", "insurance": "None"}

    # Horizontal Stats Bar
    st.markdown(f"""
        <div class="stats-container">
            <div class="stat-box"><div class="stat-label">Role</div><div class="stat-value">{stats['role']}</div></div>
            <div class="stat-box"><div class="stat-label">Cash</div><div class="stat-value green">₹{stats['cash']:,}</div></div>
            <div class="stat-box"><div class="stat-label">Savings</div><div class="stat-value green">₹{stats['savings']:,}</div></div>
            <div class="stat-box"><div class="stat-label">Debt</div><div class="stat-value red">₹{stats['debt']:,}</div></div>
            <div class="stat-box"><div class="stat-label">Invest</div><div class="stat-value purple">₹{stats['invest']:,}</div></div>
        </div>
    """, unsafe_allow_html=True)

    # Submission Logic
    if final_score is not None:
        st.write(f"### Your Final Net Worth: ₹{final_score:,}")
        with st.form("score_form"):
            username = st.text_input("Enter name for leaderboard:")
            submit = st.form_submit_button("SUBMIT SCORE")
            if submit and username.strip():
                add_score(username.strip(), final_score)
                st.success("Score added!")
                st.rerun()

    # Table Display
    rows = get_leaderboard(10)
    if rows:
        st.table([{"Rank": i+1, "Name": r[0], "Net Worth": f"₹{r[1]:,}"} for i, r in enumerate(rows)])
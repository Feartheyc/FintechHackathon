import sqlite3
import streamlit as st

DB_FILE = "leaderboard.db"

# ---------------- DB SETUP ----------------
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

# ---------------- INSERT SCORE ----------------
def add_score(username: str, net_worth: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO leaderboard (username, net_worth) VALUES (?, ?)", (username, net_worth))
    conn.commit()
    conn.close()

# ---------------- FETCH LEADERBOARD ----------------
def get_leaderboard(limit: int = 10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username, net_worth FROM leaderboard ORDER BY net_worth DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

# ---------------- STREAMLIT UI ----------------
def render_leaderboard_ui(final_score: int = None):
    init_db()
    
    st.markdown("## 🏆 Leaderboard")
    
    # Ask for username if final score is provided
    if final_score is not None:
        username = st.text_input("Enter your name for the leaderboard:")
        if st.button("Submit Score"):
            if username.strip():
                add_score(username.strip(), final_score)
                st.success(f"Score submitted! 🎉 Net Worth: ₹{final_score:,}")
                st.rerun()
            else:
                st.warning("Please enter a valid name.")
    
    # Display leaderboard
    rows = get_leaderboard(20)
    if rows:
        st.markdown("<table style='width:100%; text-align:center;'>"
                    "<tr><th>Rank</th><th>Username</th><th>Net Worth</th></tr>", unsafe_allow_html=True)
        for i, (uname, nw) in enumerate(rows, start=1):
            st.markdown(f"<tr><td>{i}</td><td>{uname}</td><td>₹{nw:,}</td></tr>", unsafe_allow_html=True)
        st.markdown("</table>", unsafe_allow_html=True)
    else:
        st.info("No scores yet. Be the first to play!")

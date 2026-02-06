import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime
from config import apply_custom_css

# ==========================================
# 0. UI CONFIGURATION
# ==========================================
st.set_page_config(page_title="Market Sim", layout="wide", page_icon="📈")
apply_custom_css()

st.markdown("<h1 style='text-align:center; margin-bottom: 30px;'>📈 NSE Stock Market Simulator</h1>", unsafe_allow_html=True)

# ==========================================
# 1. INITIALIZATION & DATABASE
# ==========================================
if "username" not in st.session_state: st.session_state.username = None

conn = sqlite3.connect("portfolio.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, cash REAL)")
c.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT, date TEXT, stock TEXT, qty INTEGER, price REAL,
    FOREIGN KEY(username) REFERENCES users(username)
)
""")
conn.commit()

# ==========================================
# 2. DATA FETCHING (CACHE)
# ==========================================
TICKERS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
    "ICICIBANK.NS", "KOTAKBANK.NS", "LT.NS", "SBIN.NS", "AXISBANK.NS",
    "BAJFINANCE.NS", "BHARTIARTL.NS", "MARUTI.NS", "ITC.NS", "ASIANPAINT.NS",
    "TATASTEEL.NS", "M&M.NS", "TITAN.NS", "WIPRO.NS", "TECHM.NS"
]

@st.cache_data(ttl=600)
def get_stock_data(tickers):
    data = {}
    for ticker in tickers:
        try:
            df = yf.Ticker(ticker).history(period="1y")
            if 'Close' in df.columns and not df.empty:
                data[ticker] = df['Close']
        except: pass
    return pd.DataFrame(data)

prices = get_stock_data(TICKERS)
if prices.empty:
    st.error("⚠️ Market Data Unavailable.")
    st.stop()

latest_prices = prices.iloc[-1]

# ==========================================
# 3. SIDEBAR (LOGIN SYSTEM)
# ==========================================
with st.sidebar:
    st.markdown("### 👤 Trader Profile")
    if st.session_state.username:
        # Fetch fresh cash balance from DB
        c.execute("SELECT cash FROM users WHERE username=?", (st.session_state.username,))
        user_cash = c.fetchone()[0]
        
        st.success(f"**{st.session_state.username}**")
        st.markdown(f"### 💳 Balance: <span style='color:#4ade80'>₹{user_cash:,.2f}</span>", unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True):
            st.session_state.username = None
            st.rerun()
    else:
        st.info("Login to access your portfolio.")
        username_input = st.text_input("Username")
        if st.button("Login / Signup", use_container_width=True):
            if username_input:
                st.session_state.username = username_input
                c.execute("SELECT cash FROM users WHERE username=?", (username_input,))
                row = c.fetchone()
                if not row:
                    # Create new user if not exists
                    c.execute("INSERT INTO users(username, cash) VALUES (?, ?)", (username_input, 10000.0))
                    conn.commit()
                    st.toast(f"Account created for {username_input}!")
                else:
                    st.toast(f"Welcome back, {username_input}!")
                st.rerun()

# ==========================================
# 4. MAIN DASHBOARD
# ==========================================
if not st.session_state.username:
    st.markdown("""
    <div class="scene-card" style="text-align:center; padding: 40px;">
        <h2>🔒 Access Restricted</h2>
        <p style="color: #94a3b8;">Please enter a username in the sidebar to access the Trading Terminal.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Re-fetch cash for main logic
c.execute("SELECT cash FROM users WHERE username=?", (st.session_state.username,))
current_cash = c.fetchone()[0]

c1, c2 = st.columns([1, 2])

with c1:
    st.markdown('<div class="scene-card">', unsafe_allow_html=True)
    st.markdown("### ⚡ Execute Trade")
    
    stock_choice = st.selectbox("Select Asset", TICKERS)
    current_price = latest_prices[stock_choice]
    
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; margin: 15px 0; text-align:center; border: 1px solid rgba(255,255,255,0.1);">
        <div style="font-size:0.8rem; color:#94a3b8; letter-spacing:1px;">CURRENT PRICE</div>
        <div style="font-size:1.8rem; font-weight:bold; color:#4ade80; font-family:'Space Mono', monospace;">₹{current_price:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    action = st.radio("Action", ["Buy", "Sell"], horizontal=True)
    quantity = st.number_input("Quantity", min_value=1, value=1)
    
    total_val = current_price * quantity
    
    if action == "Buy":
        st.caption(f"Cost: ₹{total_val:,.2f}")
    else:
        st.caption(f"Value: ₹{total_val:,.2f}")

    if st.button("Confirm Order", use_container_width=True):
        if action == "Buy":
            if total_val <= current_cash:
                new_cash = current_cash - total_val
                # Update DB
                c.execute("INSERT INTO transactions(username, date, stock, qty, price) VALUES (?, ?, ?, ?, ?)", 
                          (st.session_state.username, datetime.now().isoformat(), stock_choice, quantity, current_price))
                c.execute("UPDATE users SET cash=? WHERE username=?", (new_cash, st.session_state.username))
                conn.commit()
                st.success(f"Bought {quantity} {stock_choice}")
                st.rerun()
            else:
                st.error("❌ Insufficient Funds")
        elif action == "Sell":
            # Check holdings from DB
            c.execute("SELECT SUM(qty) FROM transactions WHERE username=? AND stock=?", (st.session_state.username, stock_choice))
            result = c.fetchone()
            total_held = result[0] if result[0] else 0
            
            if total_held >= quantity:
                new_cash = current_cash + total_val
                # Update DB (Negative quantity for sell)
                c.execute("INSERT INTO transactions(username, date, stock, qty, price) VALUES (?, ?, ?, ?, ?)", 
                          (st.session_state.username, datetime.now().isoformat(), stock_choice, -quantity, current_price))
                c.execute("UPDATE users SET cash=? WHERE username=?", (new_cash, st.session_state.username))
                conn.commit()
                st.success(f"Sold {quantity} {stock_choice}")
                st.rerun()
            else:
                st.error(f"❌ Not enough shares (Held: {total_held})")
    
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="scene-card">', unsafe_allow_html=True)
    st.markdown(f"### 📊 Market Trend: {stock_choice}")
    chart_data = prices[stock_choice]
    st.line_chart(chart_data, height=380)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PORTFOLIO SECTION (FETCHED FROM DB) ---
st.markdown('<div class="scene-card">', unsafe_allow_html=True)
st.markdown("### 💼 Your Portfolio")

# SQL Query to aggregate holdings
c.execute("""
    SELECT stock, SUM(qty) 
    FROM transactions 
    WHERE username=? 
    GROUP BY stock 
    HAVING SUM(qty) > 0
""", (st.session_state.username,))

portfolio_rows = c.fetchall()

if portfolio_rows:
    p_data = []
    total_pf_value = 0
    
    for stock, qty in portfolio_rows:
        # Safety check if ticker exists in our fetched data
        if stock in latest_prices:
            curr_price = latest_prices[stock]
            curr_val = curr_price * qty
            total_pf_value += curr_val
            
            p_data.append({
                "Stock": stock,
                "Quantity": qty,
                "Current Price": f"₹{curr_price:,.2f}",
                "Total Value": f"₹{curr_val:,.2f}"
            })
    
    if p_data:
        st.dataframe(pd.DataFrame(p_data), use_container_width=True)
        st.markdown(f"#### Total Asset Value: <span style='color:#c084fc'>₹{total_pf_value:,.2f}</span>", unsafe_allow_html=True)
    else:
        st.info("No active stocks found (Data mismatch or empty).")
else:
    st.info("You don't own any stocks yet. Start trading above!")

st.markdown('</div>', unsafe_allow_html=True)

# --- NAVIGATION ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("⬅ Return to Game Map", use_container_width=True):
    st.switch_page("app.py")
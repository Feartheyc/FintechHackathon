import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime

# --- SESSION STATE INITIALIZATION ---
if "cash" not in st.session_state:
    st.session_state.cash = 10000.0
if "transactions" not in st.session_state:
    st.session_state.transactions = []
if "username" not in st.session_state:
    st.session_state.username = None

# --- DATABASE SETUP ---
conn = sqlite3.connect("portfolio.db", check_same_thread=False)
c = conn.cursor()

# Create tables if they don't exist
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    cash REAL
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    date TEXT,
    stock TEXT,
    qty INTEGER,
    price REAL,
    FOREIGN KEY(username) REFERENCES users(username)
)
""")
conn.commit()

# --- LOGIN / LOGOUT ---
if st.session_state.username:
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        st.session_state.username = None
        st.session_state.cash = 10000.0
        st.session_state.transactions = []
        st.rerun()  # refresh page to show login form
else:
    st.sidebar.header("Login / Signup")
    username_input = st.sidebar.text_input("Username", key="username_input")
    if st.sidebar.button("Login / Signup"):
        if username_input:
            st.session_state.username = username_input
            c.execute("SELECT cash FROM users WHERE username=?", (username_input,))
            row = c.fetchone()
            if row:
                st.session_state.cash = row[0]
                c.execute("SELECT date, stock, qty, price FROM transactions WHERE username=? ORDER BY date", (username_input,))
                st.session_state.transactions = [
                    {"date": datetime.fromisoformat(r[0]), "stock": r[1], "qty": r[2], "price": r[3]}
                    for r in c.fetchall()
                ]
                st.success(f"Welcome back, {username_input}!")
            else:
                st.session_state.cash = 10000.0
                st.session_state.transactions = []
                c.execute("INSERT INTO users(username, cash) VALUES (?, ?)", (username_input, st.session_state.cash))
                conn.commit()
                st.success(f"Account created for {username_input}!")
            st.rerun()

# --- FETCH STOCK DATA ---
@st.cache_data(ttl=600)
def get_stock_data(tickers):
    data = {}
    for ticker in tickers:
        try:
            df = yf.Ticker(ticker).history(period="1y")
            if 'Close' in df.columns and not df.empty:
                data[ticker] = df['Close']
        except Exception as e:
            st.warning(f"Error fetching {ticker}: {e}")
    if not data:
        st.error("No stock data could be fetched.")
        return pd.DataFrame()
    return pd.DataFrame(data)

# --- TICKERS AND PRICES ---
TICKERS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
    "ICICIBANK.NS", "KOTAKBANK.NS", "LT.NS", "SBIN.NS", "AXISBANK.NS",
    "BAJFINANCE.NS", "BHARTIARTL.NS", "MARUTI.NS", "ITC.NS", "ASIANPAINT.NS",
    "HCLTECH.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "POWERGRID.NS", "ONGC.NS",
    "TITAN.NS", "ADANIPORTS.NS", "GRASIM.NS", "WIPRO.NS", "JSWSTEEL.NS",
    "SUNPHARMA.NS", "DRREDDY.NS", "HDFCLIFE.NS", "DIVISLAB.NS", "TECHM.NS",
    "COALINDIA.NS", "TATASTEEL.NS", "M&M.NS", "BPCL.NS", "BRITANNIA.NS",
    "IOC.NS", "CIPLA.NS", "SHREECEM.NS", "INDUSINDBK.NS", "EICHERMOT.NS"
]
prices = get_stock_data(TICKERS)
if prices.empty:
    st.stop()
latest_prices = prices.iloc[-1]

# --- TRADE SECTION ---
if st.session_state.username:
    st.sidebar.header("Trade Stocks")
    stock_choice = st.sidebar.selectbox("Select Stock", TICKERS, key="stock_choice")
    st.sidebar.write(f"Current Price: ₹{latest_prices[stock_choice]:.2f}")
    action = st.sidebar.radio("Action", ["Buy", "Sell"], key="action_choice")
    quantity = st.sidebar.number_input("Quantity", min_value=1, value=1, step=1, key="qty_input")

    if st.sidebar.button("Execute Trade", key="execute_trade"):
        price = latest_prices[stock_choice]
        if action == "Buy" and price * quantity <= st.session_state.cash:
            st.session_state.cash -= price * quantity
            tx = {"date": prices.index[-1], "stock": stock_choice, "qty": quantity, "price": price}
            st.session_state.transactions.append(tx)
            c.execute("INSERT INTO transactions(username, date, stock, qty, price) VALUES (?, ?, ?, ?, ?)",
                      (st.session_state.username, tx["date"].isoformat(), tx["stock"], tx["qty"], tx["price"]))
            c.execute("UPDATE users SET cash=? WHERE username=?", (st.session_state.cash, st.session_state.username))
            conn.commit()
            st.success(f"Bought {quantity} shares of {stock_choice} at ₹{price:.2f}")
        elif action == "Sell":
            total_held = sum(t["qty"] for t in st.session_state.transactions if t["stock"] == stock_choice)
            if total_held >= quantity:
                st.session_state.cash += price * quantity
                tx = {"date": prices.index[-1], "stock": stock_choice, "qty": -quantity, "price": price}
                st.session_state.transactions.append(tx)
                c.execute("INSERT INTO transactions(username, date, stock, qty, price) VALUES (?, ?, ?, ?, ?)",
                          (st.session_state.username, tx["date"].isoformat(), tx["stock"], tx["qty"], tx["price"]))
                c.execute("UPDATE users SET cash=? WHERE username=?", (st.session_state.cash, st.session_state.username))
                conn.commit()
                st.success(f"Sold {quantity} shares of {stock_choice} at ₹{price:.2f}")
            else:
                st.error("Not enough shares to sell!")
        else:
            st.error("Not enough cash!")

# --- PORTFOLIO SUMMARY ---
st.header("💼 Portfolio Summary")
st.write(f"Cash: ₹{st.session_state.cash:,.2f}")

portfolio = {}
for t in st.session_state.transactions:
    portfolio[t["stock"]] = portfolio.get(t["stock"], 0) + t["qty"]
portfolio = {k: v for k, v in portfolio.items() if v > 0}

total_stock_value = 0
if portfolio:
    df = pd.DataFrame([
        {"Stock": s, "Quantity": q, "Price": latest_prices[s], "Value": latest_prices[s]*q}
        for s, q in portfolio.items()
    ])
    total_stock_value = df["Value"].sum()
    st.write(df)
    st.write(f"Total Portfolio Value (Stocks Only): ₹{total_stock_value:,.2f}")
else:
    st.write("Your portfolio is empty.")

# --- PORTFOLIO VALUE OVER TIME ---
if portfolio:
    st.header("📊 Portfolio Value Over Time")
    timeline = sorted(set(t["date"] for t in st.session_state.transactions))
    plot_df = pd.DataFrame(index=timeline)
    for stock in portfolio.keys():
        values, cumulative_value = [], 0
        for date in timeline:
            txns_on_date = [t for t in st.session_state.transactions if t["stock"] == stock and t["date"] == date]
            cumulative_value += sum(t["qty"] * t["price"] for t in txns_on_date)
            values.append(cumulative_value)
        plot_df[stock] = values
    plot_df["Total"] = plot_df[list(portfolio.keys())].sum(axis=1)
    st.line_chart(plot_df)

# --- NAVIGATION BACK TO HOME ---
st.markdown("---")
if st.button("🗺️ Return to Game Map", use_container_width=True):
    # SYNC: Push current cash and portfolio value back to the game HUD before leaving
    if "game" in st.session_state:
        st.session_state.game['cash'] = int(st.session_state.cash)
        st.session_state.game['investments'] = int(total_stock_value)
        st.session_state.game['state'] = "MAP"
    st.rerun()
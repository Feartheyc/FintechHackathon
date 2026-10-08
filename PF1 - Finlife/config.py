import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');
        
        /* --- GLOBAL APP THEME --- */
        .stApp { background: radial-gradient(circle at top, #1e1b4b 0%, #020617 100%); color: #e2e8f0; font-family: 'Poppins', sans-serif; }
        
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

        /* --- MAIN MENU STYLES --- */
        .menu-title {
            text-align: center;
            font-size: 5rem;
            font-weight: 800;
            margin-top: 50px;
            background: linear-gradient(to bottom, #4ade80, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(74, 222, 128, 0.3);
            letter-spacing: -2px;
        }
        
        .menu-subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 1.2rem;
            letter-spacing: 4px;
            margin-bottom: 50px;
            text-transform: uppercase;
        }

        /* --- BUTTON STYLES --- */
        .stButton > button {
            width: 100%;
            background: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid #334155 !important;
            padding: 15px !important;
            border-radius: 12px !important;
            color: #f1f5f9 !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            text-align: left;
        }

        .stButton > button:hover {
            border-color: #4ade80 !important;
            color: #4ade80 !important;
            background: rgba(74, 222, 128, 0.1) !important;
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.4), 0 0 15px rgba(74, 222, 128, 0.2);
        }

        /* --- MENU / INFO CARD --- */
        .menu-card {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid #334155;
            padding: 40px;
            border-radius: 24px;
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        /* --- HUD BAR --- */
        .hud-container { 
            background: rgba(15, 23, 42, 0.8); 
            backdrop-filter: blur(12px); 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            border-radius: 16px; 
            padding: 15px; 
            display: flex; 
            justify-content: center; 
            flex-wrap: wrap; 
            gap: 12px; 
            margin-bottom: 25px; 
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); 
        }
        
        .hud-item { 
            text-align: center; 
            flex: 1 1 90px; 
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            padding: 8px 5px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .hud-label { 
            font-size: 0.65rem; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            color: #94a3b8; 
            font-weight: 600; 
            margin-bottom: 4px;
        }
        
        .hud-value { 
            font-family: 'Space Mono', monospace; 
            font-size: 0.95rem; 
            font-weight: 700; 
            color: #f8fafc; 
            white-space: nowrap;
        }
        
        .money-val { color: #4ade80; } 
        .debt-val { color: #f87171; } 
        .stress-val { color: #facc15; }
        .invest-val { color: #c084fc; }
        .ins-val { color: #38bdf8; }

        /* --- SCENE ELEMENTS --- */
        .scene-card { 
            background: linear-gradient(145deg, #1e293b, #0f172a); 
            border: 1px solid #334155; 
            border-radius: 20px; 
            padding: 30px; 
            margin-bottom: 20px; 
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5); 
            animation: slideUp 0.5s ease-out; 
            position: relative; 
            overflow: visible; 
        }
        .scene-card::before { 
            content: ""; 
            position: absolute; 
            top: 0; left: 0; 
            width: 100%; height: 4px; 
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899); 
            border-radius: 20px 20px 0 0;
        }

        .dialogue-box { display: flex; gap: 15px; align-items: flex-start; margin-top: 10px; }
        .avatar-box { width: 60px; height: 60px; background: #334155; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; border: 2px solid #475569; box-shadow: 0 4px 6px rgba(0,0,0,0.3); flex-shrink: 0; }
        .speech-bubble { background: #1e293b; border: 1px solid #475569; padding: 15px 20px; border-radius: 0 15px 15px 15px; color: #e2e8f0; position: relative; flex-grow: 1; }
        .speaker-name { color: #facc15; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; display: block; }
        
        .thought-container { display: flex; justify-content: flex-end; margin-top: 15px; margin-bottom: 20px; padding-right: 10px; }
        .thought-bubble { background: rgba(99, 102, 241, 0.1); border: 1px dashed #6366f1; color: #a5b4fc; padding: 10px 20px; border-radius: 15px 0 15px 15px; font-style: italic; font-size: 0.9rem; max-width: 85%; text-align: right; }
        
        .game-alert { padding: 15px; border-radius: 8px; margin-bottom: 15px; text-align: center; font-weight: bold; animation: slideUp 0.3s ease-out; border: 1px solid; }
        .alert-good { background: rgba(6, 78, 59, 0.8); border-color: #059669; color: #6ee7b7; }
        .alert-bad { background: rgba(127, 29, 29, 0.8); border-color: #dc2626; color: #fca5a5; }
        .alert-info { background: rgba(30, 58, 138, 0.8); border-color: #2563eb; color: #bfdbfe; }
        
        /* --- PERSONA SELECTION --- */
        .char-card { background-color: #1e293b; border: 2px solid #334155; border-radius: 15px; padding: 20px; text-align: center; transition: 0.3s; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: space-between; }
        .char-card:hover { transform: translateY(-5px); border-color: #38bdf8; }
        .char-img { width: 120px; height: 120px; border-radius: 50%; margin-bottom: 15px; border: 3px solid #475569; background: #0f172a; object-fit: cover; }
        
        #map-container { border: 2px solid #334155; box-shadow: 0 0 20px rgba(0,0,0,0.5); }

        /* --- FIX FOR MODALS (DIALOGS) --- */
        div[data-testid="stDialog"] {
            background-color: #1e293b;
            color: #e2e8f0;
            border: 1px solid #334155;
        }
    </style>
    """, unsafe_allow_html=True)
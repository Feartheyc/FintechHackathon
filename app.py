import streamlit as st
import base64
import streamlit.components.v1 as components

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Financial Journey", layout="wide")

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "completed_levels" not in st.session_state:
    st.session_state.completed_levels = {1}

if "current_level" not in st.session_state:
    st.session_state.current_level = 1

# -------------------------------------------------
# HANDLE LEVEL CLICK FROM SVG (QUERY PARAMS)
# -------------------------------------------------
query = st.query_params
if "level" in query:
    try:
        lvl = int(query["level"])
        if lvl in st.session_state.completed_levels:
            st.session_state.current_level = lvl
    except:
        pass

# -------------------------------------------------
# UTIL: IMAGE TO BASE64
# -------------------------------------------------
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# -------------------------------------------------
# LOAD ASSETS
# -------------------------------------------------
BG_IMG = img_to_base64("assets/map_bg.png")

# -------------------------------------------------
# ROLE-BASED MAP DATA
# -------------------------------------------------
MAPS = {
    "🌾 Farmer": {
        "nodes": {
            1: (140, 420),
            2: (360, 260),
            3: (620, 340),
            4: (900, 240),
            5: (1180, 380),
        },
        "paths": [(1, 2), (2, 3), (3, 4), (3, 5)],
    },
    "🏪 Small Business Owner": {
        "nodes": {
            1: (140, 300),
            2: (360, 420),
            3: (600, 260),
            4: (860, 420),
            5: (1120, 300),
        },
        "paths": [(1, 2), (2, 3), (3, 4), (4, 5)],
    },
    "🎓 College Student": {
        "nodes": {
            1: (160, 440),
            2: (380, 300),
            3: (620, 440),
            4: (860, 300),
            5: (1100, 440),
        },
        "paths": [(1, 2), (2, 3), (3, 4), (4, 5)],
    },
}

# -------------------------------------------------
# UI HEADER
# -------------------------------------------------
st.title("🗺️ Financial Journey")

role = st.radio(
    "Choose your role",
    ["🌾 Farmer", "🏪 Small Business Owner", "🎓 College Student"],
    horizontal=True,
)

st.divider()

# -------------------------------------------------
# BUILD MAP
# -------------------------------------------------
role_map = MAPS[role]
nodes = role_map["nodes"]
paths = role_map["paths"]

svg_parts = []

# ---- PATHS (CURVED, ORGANIC) ----
for start, end in paths:
    if start in st.session_state.completed_levels:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]

        svg_parts.append(
            f"""
            <path d="M{x1} {y1}
                     C {(x1+x2)//2} {y1-160},
                       {(x1+x2)//2} {y2+160},
                       {x2} {y2}"
                  stroke="#ffd966"
                  stroke-width="6"
                  fill="none"
                  stroke-linecap="round"/>
            """
        )

# ---- LEVEL CROSSES (CLICKABLE) ----
for level, (x, y) in nodes.items():
    unlocked = level in st.session_state.completed_levels
    color = "#ff5252" if unlocked else "#666"

    if unlocked:
        svg_parts.append(
            f"""
            <a href="?level={level}">
                <line x1="{x-14}" y1="{y-14}" x2="{x+14}" y2="{y+14}"
                      stroke="{color}" stroke-width="4" stroke-linecap="round"/>
                <line x1="{x+14}" y1="{y-14}" x2="{x-14}" y2="{y+14}"
                      stroke="{color}" stroke-width="4" stroke-linecap="round"/>
            </a>
            """
        )
    else:
        svg_parts.append(
            f"""
            <line x1="{x-14}" y1="{y-14}" x2="{x+14}" y2="{y+14}"
                  stroke="{color}" stroke-width="4" stroke-linecap="round"/>
            <line x1="{x+14}" y1="{y-14}" x2="{x-14}" y2="{y+14}"
                  stroke="{color}" stroke-width="4" stroke-linecap="round"/>
            """
        )

# ---- FINAL SVG (FIXED SCALING, NO CROPPING) ----
svg_html = f"""
<div style="overflow-x:auto;">
<svg viewBox="0 0 1400 700"
     width="1400"
     height="700"
     preserveAspectRatio="xMidYMid meet"
     style="
        background-image:url('data:image/png;base64,{BG_IMG}');
        background-size:contain;
        background-repeat:no-repeat;
        background-position:center;
        border-radius:20px;
     ">
    {''.join(svg_parts)}
</svg>
</div>
"""

components.html(svg_html, height=750)

# -------------------------------------------------
# LEVEL PANEL (NO BUTTON SELECTORS)
# -------------------------------------------------
st.divider()
st.subheader(f"❌ Level {st.session_state.current_level}")

st.info(
    f"Role: **{role}**\n\n"
    f"This is where the scenario for **Level {st.session_state.current_level}** appears.\n\n"
    f"(Choices, outcomes, learning logic come next.)"
)

if st.button("✅ Complete Level"):
    st.session_state.completed_levels.add(st.session_state.current_level + 1)
    st.success("Level completed! New path unlocked 🎉")

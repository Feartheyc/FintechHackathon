import streamlit as st

st.set_page_config(page_title="Financial Journey", layout="wide")
if "current_level" not in st.session_state:
    st.session_state.current_level = 1

if "completed_levels" not in st.session_state:
    st.session_state.completed_levels = {1}


# ------------------ GLOBAL STYLES ------------------
st.markdown(
    """
    <style>
    body {
        background-color: #0f1117;
    }

    .map-container {
        position: relative;
        width: 1600px;
        height: 600px;
        background-color: #0f1117;
        border-radius: 12px;
        padding: 40px;
    }

    .node {
        position: absolute;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #1f77ff;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 0 10px rgba(31,119,255,0.6);
    }

    .node.locked {
        background-color: #555;
        box-shadow: none;
        cursor: not-allowed;
    }

    .path {
        position: absolute;
        height: 4px;
        background-color: #1f77ff;
        opacity: 0.6;
        transform-origin: left center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------ TITLE ------------------
st.title("🗺️ Financial Journey Map")

# ------------------ ROLE SELECTION ------------------
role = st.radio(
    "Choose your role",
    ["🌾 Farmer", "🏪 Small Business Owner", "🎓 College Student"],
    horizontal=True
)

st.divider()

#--------Roles-----------------

MAPS = {
    "🌾 Farmer": {
        "nodes": {
            1: (120, 320),
            2: (360, 200),
            3: (620, 260),
            4: (880, 180),
            5: (1140, 300),
        },
        "paths": [
            (1, 2),
            (2, 3),
            (3, 4),
            (3, 5),  # branch
        ],
    },

    "🏪 Small Business Owner": {
        "nodes": {
            1: (120, 260),
            2: (320, 340),
            3: (560, 220),
            4: (800, 340),
            5: (1040, 240),
        },
        "paths": [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
        ],
    },

    "🎓 College Student": {
        "nodes": {
            1: (140, 360),
            2: (360, 260),
            3: (600, 360),
            4: (840, 260),
            5: (1080, 360),
        },
        "paths": [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
        ],
    },
}


# ------------------ MAP ------------------
role_map = MAPS[role]
nodes = role_map["nodes"]
paths = role_map["paths"]

svg_elements = []

# --- Paths ---
for start, end in paths:
    x1, y1 = nodes[start]
    x2, y2 = nodes[end]

    unlocked = start in st.session_state.completed_levels

    color = "#4da3ff" if unlocked else "#555"

    svg_elements.append(f"""
        <path d="M{x1} {y1} C {(x1+x2)//2} {y1-120}, {(x1+x2)//2} {y2+120}, {x2} {y2}"
              stroke="{color}"
              stroke-width="4"
              fill="none"
              stroke-linecap="round"
              stroke-dasharray="400"
              stroke-dashoffset="{0 if unlocked else 400}">
            <animate attributeName="stroke-dashoffset"
                     from="400" to="0"
                     dur="1.2s"
                     fill="freeze"
                     begin="0s" />
        </path>
    """)

# --- Nodes ---
for level, (x, y) in nodes.items():
    unlocked = level in st.session_state.completed_levels
    fill = "#1f77ff" if unlocked else "#555"

    svg_elements.append(f"""
        <circle cx="{x}" cy="{y}" r="30" fill="{fill}"/>
        <text x="{x}" y="{y+5}" text-anchor="middle"
              fill="white" font-size="16" font-weight="bold">
            {level}
        </text>
    """)

svg_html = f"""
<div style="overflow-x:auto;">
<svg width="1400" height="600" style="background:#0f1117; border-radius:12px;">
    {''.join(svg_elements)}
</svg>
</div>
"""

st.markdown(svg_html, unsafe_allow_html=True)


st.subheader("Select a level")

cols = st.columns(len(nodes))

for i, level in enumerate(nodes.keys()):
    unlocked = level in st.session_state.completed_levels

    if cols[i].button(
        f"Level {level}",
        disabled=not unlocked,
        key=f"level_{level}"
    ):
        st.session_state.current_level = level


st.divider()
st.subheader(f"🎯 Level {st.session_state.current_level}")

st.info(
    f"This is where the scenario for **Level {st.session_state.current_level}** will load.\n\n"
    f"Role-specific content comes here later."
)

if st.button("Mark Level as Completed"):
    next_level = st.session_state.current_level + 1
    st.session_state.completed_levels.add(next_level)



st.info("Unlocked levels are playable. Locked levels will open as you progress.")
    
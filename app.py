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

if "view" not in st.session_state:
    st.session_state.view = "map"   # "map" or "level"

# -------------------------------------------------
# HANDLE LEVEL CLICK FROM SVG (QUERY PARAMS)
# -------------------------------------------------
query = st.query_params
if "level" in query:
    try:
        lvl = int(query["level"])
        if lvl in st.session_state.completed_levels:
            st.session_state.current_level = lvl
            st.session_state.view = "level"   # 🔥 TRANSITION
            st.query_params.clear()           # 🔥 CLEAN URL
    except:
        pass

# -------------------------------------------------
# UTIL
# -------------------------------------------------
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# -------------------------------------------------
# BACKGROUNDS
# -------------------------------------------------
BG_MAPS = {
    "🌾 Farmer": img_to_base64("assets/map_farmer.png"),
    "🏪 Small Business Owner": img_to_base64("assets/map_business.png"),
    "🎓 College Student": img_to_base64("assets/map_student.png"),
}

# -------------------------------------------------
# MAP DATA
# -------------------------------------------------
MAPS = {
    "🌾 Farmer": {
        "nodes": {
            1: (140, 440),
            2: (360, 280),
            3: (620, 360),
            4: (900, 260),
            5: (1180, 400),
        },
        "paths": [(1, 2), (2, 3), (3, 4), (3, 5)],
    },
    "🏪 Small Business Owner": {
        "nodes": {
            1: (140, 300),
            2: (360, 440),
            3: (620, 260),
            4: (860, 420),
            5: (1120, 300),
        },
        "paths": [(1, 2), (2, 3), (3, 4), (4, 5)],
    },
    "🎓 College Student": {
        "nodes": {
            1: (160, 460),
            2: (380, 300),
            3: (620, 460),
            4: (860, 300),
            5: (1100, 460),
        },
        "paths": [(1, 2), (2, 3), (3, 4), (4, 5)],
    },
}

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("🗺️ Financial Journey")

role = st.radio(
    "Choose your role",
    ["🌾 Farmer", "🏪 Small Business Owner", "🎓 College Student"],
    horizontal=True,
)

st.divider()

# =================================================
# MAP VIEW
# =================================================
if st.session_state.view == "map":

    nodes = MAPS[role]["nodes"]
    paths = MAPS[role]["paths"]
    bg_img = BG_MAPS[role]

    svg_parts = []

    # ---- PATHS ----
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

    # ---- CROSSES ----
    for level, (x, y) in nodes.items():
        unlocked = level in st.session_state.completed_levels
        color = "#ff5252" if unlocked else "#666"

        cross = f"""
            <line x1="{x-14}" y1="{y-14}" x2="{x+14}" y2="{y+14}"
                  stroke="{color}" stroke-width="4" stroke-linecap="round"/>
            <line x1="{x+14}" y1="{y-14}" x2="{x-14}" y2="{y+14}"
                  stroke="{color}" stroke-width="4" stroke-linecap="round"/>
        """

        if unlocked:
            svg_parts.append(f'<a href="?level={level}">{cross}</a>')
        else:
            svg_parts.append(cross)

    svg_html = f"""
    <div style="overflow-x:auto;">
    <svg viewBox="0 0 1400 760"
         width="1400"
         height="760"
         preserveAspectRatio="xMidYMid meet"
         style="
            background-image:url('data:image/png;base64,{bg_img}');
            background-size:contain;
            background-repeat:no-repeat;
            background-position:center;
            border-radius:20px;
         ">
        {''.join(svg_parts)}
    </svg>
    </div>
    """

    components.html(svg_html, height=800)

# =================================================
# LEVEL VIEW
# =================================================
else:
    st.subheader(f"❌ Level {st.session_state.current_level}")

    st.info(
        f"Role: **{role}**\n\n"
        f"This is the gameplay screen for **Level {st.session_state.current_level}**.\n\n"
        f"(Scenario, choices, outcomes go here.)"
    )

    if st.button("⬅ Back to Map"):
        st.session_state.view = "map"

    if st.button("✅ Complete Level"):
        st.session_state.completed_levels.add(st.session_state.current_level + 1)
        st.success("Level completed! New level unlocked 🎉")

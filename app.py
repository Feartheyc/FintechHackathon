import streamlit as st
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="Financial Journey", layout="wide")

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Use ONE background for now (you can swap per role later)
BG_IMG = img_to_base64("assets/map_farmer.png")

st.title("🗺️ Financial Journey")
st.write("Choose your role (UI only for now)")

st.radio(
    "Role",
    ["🌾 Farmer", "🏪 Small Business Owner", "🎓 College Student"],
    horizontal=True,
)

components.html(
f"""
<style>
body {{
  margin: 0;
}}

#game {{
  position: relative;
  width: 100%;
  max-width: 1400px;
  margin: auto;
}}

svg {{
  width: 100%;
  height: auto;
  border-radius: 20px;
}}

.cross {{
  stroke: #ff5252;
  stroke-width: 4;
  cursor: pointer;
}}

.cross.locked {{
  stroke: #666;
  cursor: not-allowed;
}}

#modal {{
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}}

#modal-content {{
  background: #111;
  color: white;
  padding: 30px;
  border-radius: 16px;
  width: 420px;
  animation: pop 0.25s ease-out;
}}

@keyframes pop {{
  from {{ transform: scale(0.9); opacity: 0; }}
  to {{ transform: scale(1); opacity: 1; }}
}}

button {{
  margin-top: 16px;
  padding: 10px 14px;
  background: #ff5252;
  border: none;
  color: white;
  border-radius: 8px;
  cursor: pointer;
}}
</style>

<div id="game">

<svg viewBox="0 0 1400 760"
     style="
        background-image:url('data:image/png;base64,{BG_IMG}');
        background-size:contain;
        background-repeat:no-repeat;
        background-position:center;
     ">

  <!-- PATHS -->
  <path d="M140 440 C 250 280, 300 420, 360 280"
        stroke="#ffd966" stroke-width="6" fill="none" />
  <path d="M360 280 C 500 200, 560 420, 620 360"
        stroke="#ffd966" stroke-width="6" fill="none" />
  <path d="M620 360 C 760 200, 820 420, 900 260"
        stroke="#ffd966" stroke-width="6" fill="none" />

  <!-- LEVEL 1 -->
  <g onclick="openLevel(1)">
    <line x1="126" y1="426" x2="154" y2="454" class="cross"/>
    <line x1="154" y1="426" x2="126" y2="454" class="cross"/>
  </g>

  <!-- LEVEL 2 -->
  <g onclick="openLevel(2)">
    <line x1="346" y1="266" x2="374" y2="294" class="cross"/>
    <line x1="374" y1="266" x2="346" y2="294" class="cross"/>
  </g>

  <!-- LEVEL 3 -->
  <g onclick="openLevel(3)">
    <line x1="606" y1="346" x2="634" y2="374" class="cross"/>
    <line x1="634" y1="346" x2="606" y2="374" class="cross"/>
  </g>

</svg>
</div>

<!-- MODAL -->
<div id="modal">
  <div id="modal-content">
    <h2 id="modal-title"></h2>
    <p>This is where gameplay UI will go.</p>
    <button onclick="closeModal()">Close</button>
  </div>
</div>

<script>
let completedLevels = [1];

function openLevel(level) {{
  if (!completedLevels.includes(level)) {{
    alert("Level locked");
    return;
  }}
  document.getElementById("modal-title").innerText = "Level " + level;
  document.getElementById("modal").style.display = "flex";
}}

function closeModal() {{
  document.getElementById("modal").style.display = "none";
}}
</script>
""",
height=820,
)

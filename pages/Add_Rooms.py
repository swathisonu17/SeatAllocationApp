



import streamlit as st
import pandas as pd
import os

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Add Rooms", layout="wide")

# ----------------------------
# DATA FILE
# ----------------------------
DATA_FOLDER = "data"
ROOM_FILE = os.path.join(DATA_FOLDER, "rooms.csv")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# ----------------------------
# LOAD ROOMS SAFELY
# ----------------------------
if "rooms" not in st.session_state:
    if os.path.exists(ROOM_FILE) and os.path.getsize(ROOM_FILE) > 0:
        st.session_state["rooms"] = pd.read_csv(ROOM_FILE)
    else:
        st.session_state["rooms"] = pd.DataFrame(columns=["Room Name", "Capacity"])

# ----------------------------
# ✅ FIX OLD LIST ERROR
# ----------------------------
if isinstance(st.session_state["rooms"], list):
    st.session_state["rooms"] = pd.DataFrame(
        st.session_state["rooms"],
        columns=["Room Name", "Capacity"]
    )

# ----------------------------
# SAVE FUNCTION
# ----------------------------
def save_rooms():
    st.session_state["rooms"].to_csv(ROOM_FILE, index=False)

# ----------------------------
# CSS STYLING
# ----------------------------
st.markdown("""
<style>
.stApp { background-color: white !important; }
header { visibility: hidden; }

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: white !important;
    border-right: 1px solid #E5E7EB;
}
[data-testid="stSidebarNav"] ul li div a span {
    color: #1E3A8A !important;
    font-weight: 700 !important;
}

/* HEADINGS */
.main-header {
    color: #1E3A8A;
    font-size: 32px;
    font-weight: 800;
}
.sub-text {
    color: #3B82F6;
    font-size: 18px;
    margin-bottom: 25px;
}

/* BUTTON */
div.stButton > button {
    background-color: #1E3A8A !important;
    color: white !important;
    border-radius: 10px;
    border: none;
    padding: 10px 25px;
    font-weight: 600;
    width: 100%;
}

/* INPUTS */
.stTextInput input, .stNumberInput input {
    border: 2px solid #1E3A8A !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

/* TABLE */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# PAGE HEADER
# ----------------------------
st.markdown('<div class="main-header">Room Management</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Configure examination halls and seating capacities</div>', unsafe_allow_html=True)

# ----------------------------
# ROOM FORM
# ----------------------------
with st.form("room_form", clear_on_submit=True):

    col1, col2 = st.columns([3, 1])

    with col1:
        room_name = st.text_input("Room Name or Number",
                                  placeholder="e.g. Science Block - Hall 101")

    with col2:
        capacity = st.number_input("Seating Capacity",
                                   min_value=1,
                                   value=30)

    submit = st.form_submit_button("Register Room")

    if submit:
        if room_name.strip() != "":
            new_room = pd.DataFrame(
                [{"Room Name": room_name, "Capacity": capacity}]
            )

            st.session_state["rooms"] = pd.concat(
                [st.session_state["rooms"], new_room],
                ignore_index=True
            )

            save_rooms()
            st.success(f"✅ Room '{room_name}' Added Successfully!")
            st.rerun()

        else:
            st.error("❌ Please provide a valid room name.")

# ----------------------------
# DISPLAY TABLE
# ----------------------------
st.markdown("<h3 style='color:#1E3A8A;'>Registered Examination Halls</h3>",
            unsafe_allow_html=True)

if not st.session_state["rooms"].empty:

    st.dataframe(
        st.session_state["rooms"],
        hide_index=True,
        use_container_width=True
    )

else:
    st.info("No rooms have been added yet. Use the form above to register your first hall.")

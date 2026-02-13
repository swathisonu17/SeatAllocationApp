

import streamlit as st
import pandas as pd
import os

# -----------------------------
# 0. LOAD STUDENTS, ROOMS, AND PLAN FROM CSV
# -----------------------------
DATA_FOLDER = "data"
STUDENT_FILE = os.path.join(DATA_FOLDER, "students.csv")
ROOM_FILE = os.path.join(DATA_FOLDER, "rooms.csv")
PLAN_FILE = os.path.join(DATA_FOLDER, "plan.csv")

# Load students
if "students" not in st.session_state:
    if os.path.exists(STUDENT_FILE) and os.path.getsize(STUDENT_FILE) > 0:
        st.session_state["students"] = pd.read_csv(STUDENT_FILE).to_dict("records")
    else:
        st.session_state["students"] = []

# Load rooms
if "rooms" not in st.session_state:
    if os.path.exists(ROOM_FILE) and os.path.getsize(ROOM_FILE) > 0:
        st.session_state["rooms"] = pd.read_csv(ROOM_FILE).to_dict("records")
    else:
        st.session_state["rooms"] = []

# Load plan
if "plan" not in st.session_state:
    if os.path.exists(PLAN_FILE) and os.path.getsize(PLAN_FILE) > 0:
        st.session_state["plan"] = pd.read_csv(PLAN_FILE).to_dict("records")
    else:
        st.session_state["plan"] = []

# -----------------------------
# 1. PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="View Output", layout="wide")

# -----------------------------
# 2. MATCHING THEME CSS (UNCHANGED)
# -----------------------------
st.markdown("""
<style>
    .stApp { background-color: white !important; }
    header { visibility: hidden; }

    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: white !important; border-right: 1px solid #E5E7EB; }
    [data-testid="stSidebarNav"] ul li div a span { color: #1E3A8A !important; font-weight: 700 !important; }

    /* HEADINGS */
    .main-header { color: #1E3A8A !important; font-size: 32px; font-weight: 800; margin-bottom: 10px; }

    /* BLUE CARD CONTAINER */
    .custom-container {
        background-color: #F0F7FF !important;
        # padding: 25px;
        border-radius: 20px;
        border: 1px solid #D1E9FF;
        margin-bottom: 25px;
    }

    /* DARK BLUE ALERT BOX */
    .custom-alert {
        background-color: #F0F7FF;
        border-left: 5px solid #1E3A8A;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
    }

    /* INPUT LABELS */
    label, p { color: #1E3A8A !important; font-weight: 600 !important; }

    div[data-baseweb="input"] { background-color: white !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"> Examination Allotment List</div>', unsafe_allow_html=True)

# -----------------------------
# 3. CHECK IF PLAN EXISTS
# -----------------------------
if not st.session_state.get("plan"):

    st.markdown("""
        <div class="custom-alert">
            <p style="color: #1E3A8A; font-weight: 800; margin: 0; font-size: 18px;">
             NO PLAN FOUND
            </p>
            <p style="color: #1E3A8A; margin: 5px 0 0 0;">
            The database is currently empty. Please go to the 'Generate Plan' page and run the allotment first.
            </p>
        </div>
    """, unsafe_allow_html=True)

else:
    # -----------------------------
    # LOAD PLAN DATAFRAME
    # -----------------------------
    df = pd.DataFrame(st.session_state["plan"])

    # ✅ Define filtered_df properly
    filtered_df = df.copy()

    # ✅ Clean column names
    filtered_df.columns = filtered_df.columns.str.strip()

    # ✅ Force USN columns into safe string format (NO .str ERROR EVER)
    filtered_df["Student 1 USN"] = filtered_df["Student 1 USN"].apply(
        lambda x: "" if pd.isna(x) else str(x)
    )
    filtered_df["Student 2 USN"] = filtered_df["Student 2 USN"].apply(
        lambda x: "" if pd.isna(x) else str(x)
    )

    # -----------------------------
    # 4. FILTER SECTION UI (UNCHANGED)
    # -----------------------------
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        search_usn = st.text_input(" Search USN", placeholder="Enter USN...")

    with col2:
        room_list = ["All Rooms"] + sorted(filtered_df["Room"].unique().tolist())
        selected_room = st.selectbox("Filter by Room", room_list)

    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # 5. FILTER LOGIC (FIXED)
    # -----------------------------
    if search_usn:
        search_usn = search_usn.strip()

        filtered_df = filtered_df[
            (filtered_df["Student 1 USN"].str.contains(search_usn, case=False)) |
            (filtered_df["Student 2 USN"].str.contains(search_usn, case=False))
        ]

    if selected_room != "All Rooms":
        filtered_df = filtered_df[filtered_df["Room"] == selected_room]

    # -----------------------------
    # 6. DISPLAY RESULTS
    # -----------------------------
    st.markdown(
        f"<h3 style='color: #1E3A8A;'>Results ({len(filtered_df)} Rows)</h3>",
        unsafe_allow_html=True
    )

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

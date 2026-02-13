

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Upload Students", layout="wide")

# -----------------------------
# FILE PATH
# -----------------------------
DATA_FOLDER = "data"
STUDENT_FILE = os.path.join(DATA_FOLDER, "students.csv")

# Create data folder if missing
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# -----------------------------
# CSS STYLE (Same UI)
# -----------------------------
st.markdown("""
<style>
/* ✅ FORCE FULL WHITE EVERYWHERE */
html, body, [class*="css"]  {
    background-color: white !important;
    color: black !important;
}            

.stApp {
    background-color: white !important;
}

header {
    visibility: hidden;
}

/* ✅ SIDEBAR WHITE */
[data-testid="stSidebar"] {
    background-color: white !important;
    border-right: 1px solid #E5E7EB;
}

/* ✅ SIDEBAR NAV TEXT BLUE */
[data-testid="stSidebarNav"] ul li div a span {
    color: #1E3A8A !important;
    font-weight: 700 !important;
}

/* ✅ MAIN TITLE */
.main-header {
    color: #1E3A8A !important;
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 10px;
}

/* ✅ LABELS BLUE */
label {
    color: #1E3A8A !important;
    font-weight: 700 !important;
}

/* ✅ RADIO BUTTON TEXT FIX */
div[role="radiogroup"] label {
    color: black !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    opacity: 1 !important;
}

/* ✅ BUTTON STYLE */
div.stButton > button {
    background-color: #1E3A8A !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    width: auto !important;
    border: none !important;
}

/* ✅ DATAFRAME FULL WHITE */
[data-testid="stDataFrame"] {
    background-color: white !important;
    border-radius: 12px;
    padding: 10px;
    border: 1px solid #E5E7EB;
}

thead tr th {
    background-color: white !important;
    color: #1E3A8A !important;
    font-weight: 800 !important;
}

tbody tr td {
    background-color: white !important;
    color: black !important;
    font-weight: 600 !important;
}

tbody tr:hover td {
    background-color: #F9FAFB !important;
}

[data-testid="stDataFrameToolbar"] {
    display: none !important;
}
            

/* ✅ REGISTERED STUDENTS HEADING FIX */
h2, h3 {
    color: #1E3A8A !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

/* ✅ MANUAL ENTRY + BULK UPLOAD TAB FIX */
button[data-baseweb="tab"] {
    color: black !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}

/* ✅ ACTIVE TAB BLUE */
button[aria-selected="true"] {
    color: #1E3A8A !important;
    border-bottom: 3px solid #1E3A8A !important;
}

/* ✅ INPUT BOX WHITE */
.stTextInput input,
.stSelectbox select {
    background-color: white !important;
    color: black !important;
    border: 2px solid #1E3A8A !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}   

/* ✅ RADIO BUTTON TEXT FIX (Regular / Arrear Visible Always) */
div[role="radiogroup"] label {
    color: black !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    opacity: 1 !important;
}

div[role="radiogroup"] span {
    color: black !important;
    opacity: 1 !important;
}

div[role="radiogroup"] * {
    opacity: 1 !important;
}

.stRadio div {
    color: black !important;
}            

</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD STUDENTS FROM CSV (FIXED)
# -----------------------------
if "students" not in st.session_state:
    if os.path.exists(STUDENT_FILE) and os.path.getsize(STUDENT_FILE) > 0:
        st.session_state["students"] = pd.read_csv(STUDENT_FILE)
    else:
        st.session_state["students"] = pd.DataFrame(
            columns=["USN", "Name", "Sem", "Branch", "Type", "Subjects"]
        )

# ✅ EXTRA FIX: If students becomes list after refresh, convert back
if isinstance(st.session_state["students"], list):
    st.session_state["students"] = pd.DataFrame(st.session_state["students"])

# -----------------------------
# TITLE
# -----------------------------
st.markdown("<h1 class='main-header'>Student Enrollment</h1>", unsafe_allow_html=True)

# -----------------------------
# TABS
# -----------------------------
tab1, tab2 = st.tabs(["Manual Entry", "Bulk Upload (CSV)"])

# ======================================================
# ✅ TAB 1: MANUAL ENTRY
# ======================================================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        usn = st.text_input("USN / Roll No", placeholder="e.g. 1RV21CS001")
    with col2:
        name = st.text_input("Student Name", placeholder="e.g. John Doe")

    col3, col4 = st.columns(2)
    with col3:
        sem = st.selectbox("Semester", [1,2,3,4,5,6,7,8])
    with col4:
        branch = st.selectbox("Branch", ["CSE", "EEE", "ECE", "MEC", "CVL"])

    col5, col6 = st.columns(2)
    with col5:
        stype = st.radio("Student Type", ["Regular", "Arrear"], horizontal=True)
    with col6:
        subjects = st.text_input("Subjects (comma separated)", placeholder="e.g. Math, Physics")

    if st.button("Add Student"):
        if usn.strip() == "" or name.strip() == "":
            st.warning("⚠ Please enter USN and Name")
        else:
            new_student = {
                "USN": usn.upper(),
                "Name": name.title(),
                "Sem": sem,
                "Branch": branch,
                "Type": stype,
                "Subjects": subjects
            }

            st.session_state["students"] = pd.concat(
                [st.session_state["students"], pd.DataFrame([new_student])],
                ignore_index=True
            )

            st.session_state["students"].to_csv(STUDENT_FILE, index=False)

            st.success(" Student Added Successfully!")
            st.rerun()

# ======================================================
# ✅ TAB 2: BULK UPLOAD CSV
# ======================================================
with tab2:
    st.info("Upload CSV file with columns: USN, Name, Sem, Branch, Type, Subjects")

    uploaded_file = st.file_uploader("Upload Student CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        required_cols = ["USN", "Name", "Sem", "Branch", "Type", "Subjects"]

        if all(col in df.columns for col in required_cols):
            st.session_state["students"] = df
            df.to_csv(STUDENT_FILE, index=False)

            st.success(" Students Uploaded Successfully!")
            st.rerun()
        else:
            st.error("CSV must contain columns: USN, Name, Sem, Branch, Type, Subjects")

# -----------------------------
# REGISTERED STUDENTS TABLE
# -----------------------------
st.markdown("## Registered Students")

# ✅ SAFE CHECK (No refresh error)
if isinstance(st.session_state["students"], pd.DataFrame) and not st.session_state["students"].empty:
    st.dataframe(st.session_state["students"], hide_index=True, use_container_width=True)
else:
    st.info("No students registered yet.")

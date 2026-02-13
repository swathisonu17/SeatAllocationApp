

import streamlit as st
import pandas as pd
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Generate Plan", layout="wide")

# -----------------------------
# FILE PATHS
# -----------------------------
DATA_FOLDER = "data"
STUDENT_FILE = os.path.join(DATA_FOLDER, "students.csv")
ROOM_FILE = os.path.join(DATA_FOLDER, "rooms.csv")

# -----------------------------
# LOAD STUDENTS FROM CSV
# -----------------------------
if "students" not in st.session_state:
    if os.path.exists(STUDENT_FILE) and os.path.getsize(STUDENT_FILE) > 0:
        st.session_state["students"] = pd.read_csv(STUDENT_FILE).to_dict("records")
    else:
        st.session_state["students"] = []

# -----------------------------
# LOAD ROOMS FROM CSV
# -----------------------------
if "rooms" not in st.session_state:
    if os.path.exists(ROOM_FILE) and os.path.getsize(ROOM_FILE) > 0:
        st.session_state["rooms"] = pd.read_csv(ROOM_FILE).to_dict("records")
    else:
        st.session_state["rooms"] = []

# -----------------------------
# INIT PLAN
# -----------------------------
if "plan" not in st.session_state:
    st.session_state["plan"] = []

# -----------------------------
# CSS THEME (Same All Pages)
# -----------------------------
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

/* TITLE */
.main-header {
    color: #1E3A8A !important;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 15px;
}

/* INFO BOX */
.custom-alert {
    background-color: #F0F7FF;
    border-left: 5px solid #1E3A8A;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 25px;
}

/* BUTTON */
div.stButton > button {
    background-color: #1E3A8A !important;
    color: white !important;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: bold;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #2563EB !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid #E5E7EB;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# PAGE TITLE
# -----------------------------
st.markdown("<div class='main-header'>Seat Allotment Generator</div>", unsafe_allow_html=True)

# -----------------------------
# FETCH DATA
# -----------------------------
students = st.session_state["students"]
rooms = st.session_state["rooms"]
# ✅ FIX: If rooms is DataFrame convert to dict records
if isinstance(rooms, pd.DataFrame):
    rooms = rooms.to_dict("records")
# ✅ FIX STUDENTS FORMAT (extra safety)
if isinstance(students, pd.DataFrame):
    students = students.to_dict("records")    

# -----------------------------
# VALIDATION CHECK
# -----------------------------
if len(students) == 0 or len(rooms) == 0:
    st.markdown(f"""
    <div class="custom-alert">
        <h3 style="color:#1E3A8A; margin:0;">⚠️ Data Missing</h3>
        <p style="color:#1E3A8A; margin:5px 0 0 0;">
        Please upload Students and Rooms before generating the plan.<br>
        Currently Found: <b>{len(students)}</b> students, <b>{len(rooms)}</b> rooms.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# -----------------------------
# READY CARD
# -----------------------------
st.markdown(f"""
<div class="custom-alert">
    <h3 style="color:#1E3A8A; margin:0;"> Ready to Generate</h3>
    <p style="color:#1E3A8A; margin-top:5px;">
    Total Students: <b>{len(students)}</b><br>
    Total Rooms: <b>{len(rooms)}</b>
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# SEATING CONFIGURATION
# -----------------------------
st.markdown("""
<h3 style="color:#1E3A8A; font-weight:400; margin-top:10px;">
 Seating Configuration:-Select No of Students in each bench
</h3>
""", unsafe_allow_html=True)

seating_mode = st.selectbox(
    "How many students per bench?",
    [1, 2],
    index=0
)


# -----------------------------
# GENERATE BUTTON
# -----------------------------

if st.button(" Run Smart Seat Allotment"):

    # -----------------------------
    # STEP 1: MIX STUDENTS BY BRANCH
    # -----------------------------
    branches = {}

    for s in students:
        branch = s.get("Branch", "Other")
        branches.setdefault(branch, []).append(s)

    mixed_students = []
    max_len = max(len(lst) for lst in branches.values())

    for i in range(max_len):
        for b in branches:
            if i < len(branches[b]):
                mixed_students.append(branches[b][i])

    total_students = len(mixed_students)

    # -----------------------------
    # STEP 2: CHECK TOTAL CAPACITY
    # -----------------------------
    total_benches = sum(int(r["Capacity"]) for r in rooms)
    # total_capacity = total_benches * 2  # Max 2 students per bench
    total_capacity = total_benches * seating_mode


    if total_capacity < total_students:
        st.error(f"""
        ❌ Not enough benches!

        Total Students = {total_students}
        Total Benches = {total_benches}
        Max Capacity (2 per bench) = {total_capacity}

        Please add more rooms.
        """)
        st.stop()

    # -----------------------------
    # STEP 3: ALLOTMENT (1 OR 2 PER BENCH)
    # -----------------------------
    final_plan = []
    idx = 0
    serial = 1

    for r in rooms:

        room_name = r["Room Name"]
        # benches = int(r["Capacity"])
        benches = int(r.get("Capacity", 0))
        capacity = benches * seating_mode

        for bench_no in range(1, benches + 1):

            if idx >= total_students:
                break

            # Student 1 always sits
            s1 = mixed_students[idx]
            idx += 1

            # Student 2 sits only if available
            s2 = None
            if seating_mode == 2 and idx < total_students:
                s2 = mixed_students[idx]
                idx += 1

                # Try to avoid same branch pairing
                if s1.get("Branch") == s2.get("Branch"):
                    if idx < total_students:
                        swap_student = mixed_students[idx]
                        mixed_students[idx] = s2
                        s2 = swap_student

            # Save bench seating
            final_plan.append({
                "S.No": serial,
                "Room": room_name,
                "Bench": bench_no,

                "Student 1 USN": s1.get("USN"),
                "Student 1 Name": s1.get("Name"),
                "Student 1 Branch": s1.get("Branch"),

                "Student 2 USN": s2.get("USN") if s2 else "-",
                "Student 2 Name": s2.get("Name") if s2 else "-",
                "Student 2 Branch": s2.get("Branch") if s2 else "-",
            })

            serial += 1

    # -----------------------------
    # STEP 4: SAVE PLAN
    # -----------------------------
    with st.spinner("Generating Seat Allotment Plan... Please wait"):
     st.session_state["plan"] = final_plan

    # st.success("✅ Seat Plan Generated Successfully!")


    # -----------------------------
    # STEP 4: SAVE PLAN
    # -----------------------------
    with st.spinner("Generating Seat Allotment Plan... Please wait"):
      st.session_state["plan"] = final_plan

      # ✅ SAVE PLAN TO CSV (IMPORTANT)
      PLAN_FILE = os.path.join("data", "plan.csv")
      pd.DataFrame(final_plan).to_csv(PLAN_FILE, index=False)

    st.success("✅ Seat Plan Generated + Saved Successfully!")
  

# -----------------------------
# PREVIEW OUTPUT
# -----------------------------
if "plan" in st.session_state and len(st.session_state["plan"]) > 0:

    st.markdown("""
    <h3 style="color:#1E3A8A; font-weight:800; margin-top:30px;">
    Generated Seat Plan Preview
    </h3>
    """, unsafe_allow_html=True)


    preview_df = pd.DataFrame(st.session_state["plan"])

    st.dataframe(preview_df, hide_index=True, use_container_width=True)

    st.info("➡ Now go to **Download Report Page** to export the full report.")





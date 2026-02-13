
import streamlit as st
import pandas as pd
import os

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Download Report", layout="wide")

# ---------------------------
# STYLING (Only UI Improved)
# ---------------------------
st.markdown("""
<style>

    /* Background */
    .stApp {
        background-color: #F8FAFC !important;
    }

    header {
        visibility: hidden;
    }
    
    /* ---------------- SIDEBAR FIX ---------------- */

    section[data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 2px solid #E5E7EB;
    }

    section[data-testid="stSidebar"] * {
        color: #1E3A8A !important;
        font-weight: 600;
    }

    /* Sidebar menu selected item */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        padding: 8px;
        border-radius: 10px;
        transition: 0.2s;
    }

    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background: #EFF6FF !important;
    }
        

    /* Main Title Box */
    .report-header {
        background: linear-gradient(to right, #1E3A8A, #2563EB);
        color: white;
        padding: 5px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 25px;
        font-size: 28px;
        font-weight: bold;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
    }

    /* Table Styling */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
    }

    /* Download Button Styling */
    div.stDownloadButton > button {
        background: #1E3A8A !important;
        color: white !important;
        font-size: 17px !important;
        font-weight: bold !important;
        padding: 12px !important;
        border-radius: 12px !important;
        border: none !important;
        width: auto !important;
        transition: 0.3s;
    }

    div.stDownloadButton > button:hover {
        background: #2563EB !important;
        transform: scale(1.02);
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown(
    '<div class="report-header">Download Seat Allotment Report</div>',
    unsafe_allow_html=True
)

# ---------------------------
# HELPER FUNCTION
# ---------------------------
def ensure_dataframe(obj, columns):
    if isinstance(obj, list):
        df = pd.DataFrame(obj)
    elif isinstance(obj, pd.DataFrame):
        df = obj.copy()
    else:
        df = pd.DataFrame()

    for col in columns:
        if col not in df.columns:
            df[col] = ""

    return df[columns]


# ---------------------------
# SESSION STATE INIT
# ---------------------------
# if "plan" not in st.session_state:
#     st.session_state["plan"] = pd.DataFrame()
# ✅ FIX: Ensure plan is always DataFrame
if "plan" not in st.session_state or not isinstance(st.session_state["plan"], pd.DataFrame):
    st.session_state["plan"] = pd.DataFrame()


# ---------------------------
# LOAD STUDENTS CSV
# ---------------------------
students_columns = ["USN", "Name", "Sem", "Branch", "Type", "Subjects"]
students_path = os.path.join("data", "students.csv")

if os.path.exists(students_path):
    students_df = pd.read_csv(students_path)
    students_df.columns = students_df.columns.str.strip()
    students_df = ensure_dataframe(students_df, students_columns)
    students_df = pd.read_csv(students_path)
    # Clean column names
    students_df.columns = students_df.columns.str.strip()

    # Auto-fix common column mistakes
    students_df.rename(columns={
      "USN ": "USN",
      "Name ": "Name",
      "Branch ": "Branch"
    }, inplace=True)
    students_df = ensure_dataframe(students_df, students_columns)

else:
    students_df = pd.DataFrame(columns=students_columns)

# ---------------------------
# LOAD ROOMS CSV
# ---------------------------
rooms_columns = ["Name", "Capacity"]
rooms_path = os.path.join("data", "rooms.csv")

if os.path.exists(rooms_path):
    rooms_df = pd.read_csv(rooms_path)
    rooms_df.columns = rooms_df.columns.str.strip()
    rooms_df = ensure_dataframe(rooms_df, rooms_columns)
    rooms_df = pd.read_csv(rooms_path)
    # Clean column names
    rooms_df.columns = rooms_df.columns.str.strip()
    # Auto-fix common room header mistakes
    rooms_df.rename(columns={
      "Room": "Name",
      "Room Name": "Name",
      "room": "Name",
      "capacity ": "Capacity"
    }, inplace=True)
    rooms_df = ensure_dataframe(rooms_df, rooms_columns)


    rooms_df["Capacity"] = pd.to_numeric(
        rooms_df["Capacity"], errors="coerce"
    ).fillna(0).astype(int)

else:
    rooms_df = pd.DataFrame(columns=rooms_columns)

# ---------------------------
# GENERATE SEAT PLAN (Same Logic)
# ---------------------------
if st.session_state["plan"].empty and not students_df.empty and not rooms_df.empty:

    plan_list = []
    student_index = 0
    serial = 1

    for _, room in rooms_df.iterrows():
        room_name = room["Name"]
        capacity = room["Capacity"]

        for _ in range(capacity):
            if student_index >= len(students_df):
                break

            student = students_df.iloc[student_index]

            plan_list.append({
                "S.No": serial, 
                "USN": student["USN"],
                "Name": student["Name"],
                "Sem": student["Sem"],
                "Branch": student["Branch"],
                "Type": student["Type"],
                "Subjects": student["Subjects"],
                "Room": room_name
            })

            student_index += 1

    st.session_state["plan"] = pd.DataFrame(plan_list)

# ---------------------------
# DISPLAY REPORT
# ---------------------------
if st.session_state["plan"].empty:
    st.warning("⚠️ No report available. Please upload Students and Rooms first.")
    st.stop()

df = st.session_state["plan"]

st.success("✅ Seat Allotment Report Generated Successfully!")

# ---------------------------
# FULL REPORT TABLE (Directly Below Success Message)
# ---------------------------
st.subheader("Final Seat Allotment Report")

st.dataframe(
    df,
    hide_index=True,
    use_container_width=True
)

# ---------------------------
# DOWNLOAD BUTTON BELOW TABLE
# ---------------------------
csv_data = df.to_csv(index=False).encode("utf-8")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 2, 3])

with col2:
    st.download_button(
        label="⬇ Download Report",
        data=csv_data,
        file_name="Exam_Seat_Allotment_Report.csv",
        mime="text/csv"
    )


# ---------------------------
# SUMMARY TABLES
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Room Wise Summary")
    summary = df.groupby("Room").size().reset_index(name="Student Count")
    st.table(summary.reset_index(drop=True))


with col2:
    st.subheader("Department Wise Summary")
    dept_summary = df.groupby("Branch").size().reset_index(name="Count")
    st.table(dept_summary.reset_index(drop=True))


st.divider()






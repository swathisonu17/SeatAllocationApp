import streamlit as st
import pandas as pd
import os

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# -----------------------------
# FILE PATHS
# -----------------------------
DATA_FOLDER = "data"
PLAN_FILE = os.path.join(DATA_FOLDER, "plan.csv")

st.markdown("""
<style>
# .stApp {
#     background-color: white !important;
#     color: black !important;
# }

# h1, h2, h3, h4, h5, h6, p, label {
#     color: black !important;
# }

# table {
#     background-color: white !important;
#     color: black !important;
# }
            
/* Remove Streamlit top black header */
header {
    visibility: hidden;
}

/* Remove extra top padding */
.block-container {
    padding-top: 30px !important;
}

/* Main background */
.stApp {
    background-color: white !important;
}

/* Sidebar Blue */
section[data-testid="stSidebar"] {
    background-color: white !important;
}

/* Sidebar text white */
section[data-testid="stSidebar"] * {
    # color: white !important;
    color: #1E3A8A !important;        
    font-weight: 700 !important; 
}

/* Sidebar selected item highlight */
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    padding: 8px;
    border-radius: 8px;
}

/* Title Blue */
h1 {
    color: #0B4DA2 !important;
    font-weight: bold;
}

/* Button Styling */
.stButton button {
    background-color: #0B4DA2 !important;
    color: white !important;
    border-radius: 10px;
    padding: 10px 18px;
    font-size: 15px;
}

.stButton button:hover {
    background-color: #08356F !important;
    transform: scale(1.02);
}            

            
</style>
""", unsafe_allow_html=True)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Hall Report PDF", layout="wide")

st.title(" Hall Seating Report")

# -----------------------------
# CHECK PLAN FILE
# -----------------------------
if not os.path.exists(PLAN_FILE) or os.path.getsize(PLAN_FILE) == 0:
    st.error(" Seating Plan not found. Please Generate Plan first.")
    st.stop()

# -----------------------------
# LOAD PLAN FILE
# -----------------------------
plan_df = pd.read_csv(PLAN_FILE)
plan_df.columns = plan_df.columns.str.strip()

# -----------------------------
# ROOM DROPDOWN
# -----------------------------
rooms = plan_df["Room"].unique().tolist()

selected_room = st.selectbox(" Select Room for PDF Report", rooms)

room_df = plan_df[plan_df["Room"] == selected_room]

# -----------------------------
# PDF FUNCTION (Only USN Report)
# -----------------------------
def generate_pdf(room_name, room_data):
    filename = f"Hall_Report_{room_name}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # -----------------------------
    # TITLE
    # -----------------------------
    elements.append(Paragraph("EXAM HALL SEATING REPORT", styles["Title"]))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph(f"Room Name: {room_name}", styles["Heading2"]))
    elements.append(Spacer(1, 20))

    # -----------------------------
    # TABLE HEADER (Only USN + Branch)
    # -----------------------------
    table_data = [["Bench No", "USN", "Branch"]]

    # -----------------------------
    # ADD STUDENTS ROW-WISE
    # -----------------------------
    for _, row in room_data.iterrows():

        bench = row["Bench"]

        usn1 = str(row["Student 1 USN"]).strip()
        branch1 = str(row["Student 1 Branch"]).strip()

        # Add Student 1
        if usn1 != "-" and usn1 != "":
            table_data.append([bench, usn1, branch1])

        usn2 = str(row["Student 2 USN"]).strip()
        branch2 = str(row["Student 2 Branch"]).strip()

        # Add Student 2 (as separate row)
        if usn2 != "-" and usn2 != "":
            table_data.append([bench, usn2, branch2])

    # -----------------------------
    # CREATE TABLE
    # -----------------------------
    table = Table(table_data, colWidths=[90, 200, 150])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("FONTSIZE", (0, 1), (-1, -1), 11),
    ]))

    elements.append(table)

    # -----------------------------
    # SIGNATURE
    # -----------------------------
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("Supervisor Signature: ____________________", styles["Normal"]))

    doc.build(elements)

    return filename



# -----------------------------
# BUTTON (ONLY PDF DOWNLOAD)
# -----------------------------
if st.button(" Generate Supervisor Hall Report PDF"):

    pdf_file = generate_pdf(selected_room, room_df)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="⬇ Download PDF Report",
            data=f,
            file_name=pdf_file,
            mime="application/pdf"
        )

    st.success("✅ Hall Report PDF Generated Successfully!")

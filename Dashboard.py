
import streamlit as st
import base64
import pandas as pd
import os

# ----------------------------
# 0. LOAD STUDENTS & ROOMS FROM CSV
# ----------------------------
DATA_FOLDER = "data"
PLAN_FILE = os.path.join(DATA_FOLDER, "plan.csv")
STUDENT_FILE = os.path.join(DATA_FOLDER, "students.csv")
ROOM_FILE = os.path.join(DATA_FOLDER, "rooms.csv")

# Load students into session_state
if os.path.exists(STUDENT_FILE) and os.path.getsize(STUDENT_FILE) > 0:
    st.session_state['students'] = pd.read_csv(STUDENT_FILE).to_dict('records')
else:
    st.session_state['students'] = []

# Load rooms into session_state
if os.path.exists(ROOM_FILE) and os.path.getsize(ROOM_FILE) > 0:
    st.session_state['rooms'] = pd.read_csv(ROOM_FILE).to_dict('records')
else:
    st.session_state['rooms'] = []

# ----------------------------
# 1. PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Exam Management", layout="wide")

# ----------------------------
# 2. IMAGE HANDLING
# ----------------------------
def get_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

seat_img = get_base64("seat.png") 

# ----------------------------
# 3. DATA LOGIC
# ----------------------------
total_students = len(st.session_state.get('students', []))
total_rooms = len(st.session_state.get('rooms', []))
total_capacity = sum([r.get('Capacity', 0) for r in st.session_state.get('rooms', [])])
status = "Generated" if os.path.exists(PLAN_FILE) and os.path.getsize(PLAN_FILE) > 0 else "Not Generated"


# ----------------------------
# 4. CSS FOR NAVY BLUE THEME
# ----------------------------
st.markdown("""
<style>
    /* MAIN BACKGROUND */
    .stApp { background-color: white !important; }
    header { visibility: hidden; }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] { 
        background-color: white !important; 
        border-right: 1px solid #E5E7EB; 
    }
    [data-testid="stSidebarNav"] li a span { 
        color: #1E3A8A !important; 
        font-weight: 700 !important; 
    }

    /* 1. TOP BOX - PALE BLUE (AS IN IMAGE) */
    .hero-container {
         background: #F0F7FF !important; 
         border: 1px solid #D1E9FF;
         border-radius: 20px;
         padding: 23px 40px;
         display: flex;
         justify-content: space-between;
         align-items: center;
         height: 150px; 
         margin-top:-60px;
         margin-bottom: -56px;     
        }

    .hero-title { 
        color: #1E3A8A !important; 
        font-size: 32px; 
        font-weight: 800; 
        white-space: nowrap; 
    }

    /* IMAGE FITTING */
    .img-side img { 
            height: 130px; 
            width: 100%; 
            object-fit: cover !important;
            opacity: 0.97;
            border-radius: 20px; 
            }

    /* WHITE METRIC CARDS */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .m-title { color: #64748B; font-weight: 700; font-size: 13px; text-transform: uppercase; }
    .m-val { color: #1E3A8A; font-size: 30px; font-weight: 800; }
    .m-status { color: #EF4444; font-size: 22px; font-weight: 800; }

    /* 2. BOTTOM BOX - EXACT NAVY BLUE */
    .info-box-blue {
        background-color: #1E3A8A !important; /* Deep Navy Blue */
        padding: 45px;
        border-radius: 20px;
        color: #FFFFFF !important;
        margin-top: 25px;
        height:210px;
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.2);
    }
    .info-box-blue h1 { 
        color: #FFFFFF !important; 
        font-size: 30px; 
        font-weight: 700; 
        border: none; 
        margin-bottom: 10px; 
    }
    .info-box-blue p { 
        color: #FFFFFF !important; 
        font-size: 17px; 
        line-height: 1.6; 
        opacity: 0.9;
    }
            

            
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 5. DASHBOARD LAYOUT
# ----------------------------
st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">Welcome to Exam Seat Allotment System</div>
    <div class="img-side"><img src="data:image/png;base64,{seat_img}"></div>
</div>
""", unsafe_allow_html=True)

st.write("##")
# Status Color Logic
status_color = "#EF4444" if status == "Not Generated" else "#22C55E"


# Metric Cards
c1, c2, c3, c4 = st.columns(4, gap="medium")
with c1: 
    st.markdown(f"<div class='metric-card'><div class='m-title'>Total Students</div><div class='m-val'>{total_students}</div></div>", unsafe_allow_html=True)
with c2: 
    st.markdown(f"<div class='metric-card'><div class='m-title'>Rooms Added</div><div class='m-val'>{total_rooms}</div></div>", unsafe_allow_html=True)
with c3: 
    st.markdown(f"<div class='metric-card'><div class='m-title'>Total Capacity</div><div class='m-val'>{total_capacity}</div></div>", unsafe_allow_html=True)
# 
with c4: 
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='m-title'>Status</div>
            <div style='color:{status_color}; font-size:22px; font-weight:800;'>
                {status}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Bottom Navy Box
st.markdown("""
<div class="info-box-blue">
    <h1>Seat Allotment Automation System</h1>
    <p>Automatically allocates students into halls while mixing departments to prevent clashes and ensure a smooth exam process.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Make space at bottom so footer doesn't overlap */
.main {
    padding-bottom: 60px;
}

/* Footer container */
.footer-container {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: white;
    overflow: hidden;
    border-top: 1px solid #ddd;
    z-index: 99999;
}

/* Scrolling text */
.footer-text {
    display: inline-block;
    white-space: nowrap;
    padding-left: 100%;
    font-size: 16px;
    font-weight: 600;
    color: blue;
    animation: scroll-left 20s linear infinite;
}

/* Animation */
@keyframes scroll-left {
    0% {
        transform: translateX(0%);
    }
    100% {
        transform: translateX(-100%);
    }
}
</style>

<div class="footer-container">
    <div class="footer-text">
        Designed and Developed by Swathi H | All Rights Reserved © 2026 
</div>
""", unsafe_allow_html=True)

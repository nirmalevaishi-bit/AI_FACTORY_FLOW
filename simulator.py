import streamlit as st
import csv
import os
import random
import time
import math
from datetime import datetime

# ============================================================
# STREAMLIT CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Virtual Bearing Manufacturing Factory",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATASET_FILE = "factory_live_dataset.csv"

CSV_HEADERS = [
    "Timestamp",
    "Machine_ID",
    "Process_Name",
    "Temperature_C",
    "Vibration_mm_s",
    "Speed_RPM",
    "Output_Units",
    "Defects",
    "Status"
]

# ============================================================
# FACTORY CONFIGURATION
# ============================================================

FACTORY_SECTIONS = [
    {
        "id": "M1",
        "name": "Turning",
        "short": "TURNING",
        "temperature": 42.0,
        "vibration": 0.8,
        "speed": 1200
    },
    {
        "id": "M2",
        "name": "Heat Treatment",
        "short": "HEAT",
        "temperature": 72.0,
        "vibration": 0.4,
        "speed": 0
    },
    {
        "id": "M3",
        "name": "Grinding & Honing",
        "short": "GRINDING",
        "temperature": 58.0,
        "vibration": 1.5,
        "speed": 950
    },
    {
        "id": "M4",
        "name": "Assembly",
        "short": "ASSEMBLY",
        "temperature": 62.0,
        "vibration": 0.5,
        "speed": 700
    },
    {
        "id": "M5",
        "name": "Quality Inspection",
        "short": "QUALITY",
        "temperature": 45.0,
        "vibration": 0.3,
        "speed": 500
    },
    {
        "id": "M6",
        "name": "Packaging",
        "short": "PACKING",
        "temperature": 45.0,
        "vibration": 0.3,
        "speed": 850
    }
]

# ============================================================
# SESSION STATE
# ============================================================

if "factory_running" not in st.session_state:
    st.session_state.factory_running = False

if "cycle" not in st.session_state:
    st.session_state.cycle = 0

if "last_record_time" not in st.session_state:
    st.session_state.last_record_time = 0.0

if "total_produced" not in st.session_state:
    st.session_state.total_produced = 0

if "total_defects" not in st.session_state:
    st.session_state.total_defects = 0

if "total_anomalies" not in st.session_state:
    st.session_state.total_anomalies = 0

if "last_record" not in st.session_state:
    st.session_state.last_record = None

# ============================================================
# CSV INITIALIZATION
# ============================================================

def initialize_csv():
    if not os.path.exists(DATASET_FILE):
        with open(
            DATASET_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)

initialize_csv()

# ============================================================
# GENERATE ONE LIVE FACTORY RECORD
# ============================================================

def generate_live_record():

    section = random.choice(FACTORY_SECTIONS)

    # About 18% chance of anomaly
    anomaly = random.random() < 0.18

    if anomaly:

        temperature = round(
            section["temperature"] + random.uniform(15, 25),
            2
        )

        vibration = round(
            section["vibration"] + random.uniform(3.0, 6.0),
            2
        )

        if section["speed"] == 0:
            speed = 0
        else:
            speed = max(
                0,
                section["speed"] - random.randint(200, 400)
            )

        defects = random.randint(1, 4)

        status = "WARNING"

    else:

        temperature = round(
            section["temperature"] + random.uniform(-2, 3),
            2
        )

        vibration = round(
            max(
                0.1,
                section["vibration"] + random.uniform(-0.15, 0.35)
            ),
            2
        )

        if section["speed"] == 0:
            speed = 0
        else:
            speed = (
                section["speed"]
                + random.randint(-20, 20)
            )

        defects = 0

        status = "RUNNING"

    record = {
        "Timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "Machine_ID": section["id"],
        "Process_Name": section["name"],
        "Temperature_C": temperature,
        "Vibration_mm_s": vibration,
        "Speed_RPM": speed,
        "Output_Units": 1,
        "Defects": defects,
        "Status": status
    }

    return record

# ============================================================
# SAVE LIVE RECORD
# ============================================================

def save_record(record):

    with open(
        DATASET_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            record["Timestamp"],
            record["Machine_ID"],
            record["Process_Name"],
            record["Temperature_C"],
            record["Vibration_mm_s"],
            record["Speed_RPM"],
            record["Output_Units"],
            record["Defects"],
            record["Status"]
        ])

# ============================================================
# READ DATA
# ============================================================

def read_data():

    records = []

    if not os.path.exists(DATASET_FILE):
        return records

    try:

        with open(
            DATASET_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                try:

                    row["Temperature_C"] = float(
                        row["Temperature_C"]
                    )

                    row["Vibration_mm_s"] = float(
                        row["Vibration_mm_s"]
                    )

                    row["Speed_RPM"] = float(
                        row["Speed_RPM"]
                    )

                    row["Output_Units"] = int(
                        float(row["Output_Units"])
                    )

                    row["Defects"] = int(
                        float(row["Defects"])
                    )

                    records.append(row)

                except Exception:
                    continue

    except Exception:
        return []

    return records

# ============================================================
# DARK DASHBOARD THEME
# ============================================================

st.markdown(
    """
<style>

/* =========================
   MAIN STREAMLIT BACKGROUND
   ========================= */

.stApp {
    background:
        radial-gradient(
            circle at 20% 10%,
            #183746 0%,
            #0b1720 35%,
            #071018 70%,
            #050b10 100%
        );

    color: #eafcff;
}

/* Main content */

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* =========================
   MAIN TITLE
   ========================= */

.main-title {
    text-align: center;

    color: #7deaff;

    font-size: 35px;

    font-weight: 900;

    letter-spacing: 1.5px;

    text-shadow:
        0 0 8px rgba(67,220,255,.45),
        0 0 20px rgba(67,220,255,.20);
}

.main-subtitle {
    text-align: center;

    color: #9ab8c2;

    font-size: 14px;

    margin-bottom: 18px;
}

/* =========================
   STREAMLIT TEXT
   ========================= */

h1, h2, h3, h4, h5, h6 {

    color: #e9fbff !important;

}

p, label, span {

    color: #d4e8ed;

}

/* =========================
   STATUS CARDS
   ========================= */

.info-card {

    background:
        linear-gradient(
            145deg,
            #132a35,
            #0b1c25
        );

    border-radius: 18px;

    padding: 18px;

    border: 1px solid #275363;

    box-shadow:
        0 8px 25px rgba(0,0,0,.45),
        inset 0 0 20px rgba(50,190,220,.04);

    min-height: 105px;
}

.info-title {

    color: #7fa6b2;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: .7px;
}

.info-value {

    color: #7deaff;

    font-size: 25px;

    font-weight: 900;

    margin-top: 8px;

    text-shadow:
        0 0 10px rgba(60,220,255,.25);
}

/* =========================
   AI CARD
   ========================= */

.ai-card {

    background:
        linear-gradient(
            145deg,
            #102d2b,
            #0a1c1d
        );

    border-left: 7px solid #27e59b;

    border-radius: 15px;

    padding: 18px;

    box-shadow:
        0 8px 25px rgba(0,0,0,.45),
        0 0 20px rgba(39,229,155,.06);

    color: #dffef4;
}

.ai-card b {

    color: #42efad;

    font-size: 16px;
}

/* =========================
   SECTION CARDS
   ========================= */

.section-card {

    background:
        linear-gradient(
            145deg,
            #142a34,
            #091820
        );

    border-radius: 15px;

    border: 1px solid #315968;

    padding: 14px;

    text-align: center;

    color: #dff7fc;

    box-shadow:
        0 7px 20px rgba(0,0,0,.4);

    min-height: 125px;
}

.section-card b {

    color: #70ddf0;

}

/* =========================
   METRICS
   ========================= */

[data-testid="stMetric"] {

    background:
        linear-gradient(
            145deg,
            #132934,
            #0b1921
        );

    border: 1px solid #2c5260;

    border-radius: 15px;

    padding: 15px;

    box-shadow:
        0 7px 20px rgba(0,0,0,.4);
}

[data-testid="stMetricLabel"] {

    color: #8faeb7 !important;

}

[data-testid="stMetricValue"] {

    color: #72eaff !important;

}

/* =========================
   BUTTONS
   ========================= */

.stButton > button {

    background:
        linear-gradient(
            135deg,
            #146c7d,
            #0c4352
        );

    color: #ffffff;

    border: 1px solid #38cbe8;

    border-radius: 12px;

    font-weight: 800;

    padding: 10px;

    box-shadow:
        0 0 12px rgba(45,210,240,.18);

    transition:
        .2s ease;
}

.stButton > button:hover {

    background:
        linear-gradient(
            135deg,
            #1a879b,
            #0e5263
        );

    border-color: #72eeff;

    box-shadow:
        0 0 20px rgba(50,220,245,.35);

    transform:
        translateY(-2px);
}

/* =========================
   PROGRESS BAR
   ========================= */

.stProgress > div > div {

    background-color: #162a33;

    border-radius: 20px;
}

.stProgress > div > div > div {

    background:
        linear-gradient(
            90deg,
            #18d69a,
            #4be8ff
        );

    box-shadow:
        0 0 12px rgba(60,230,210,.35);
}

/* =========================
   ALERT BOXES
   ========================= */

[data-testid="stAlert"] {

    border-radius: 12px;

}

/* =========================
   FACTORY OUTER FRAME
   ========================= */

.factory-wrapper {

    background:
        linear-gradient(
            145deg,
            #152d38,
            #08151d
        );

    border-radius: 25px;

    padding: 10px;

    border: 1px solid #2b5a68;

    box-shadow:
        0 15px 45px rgba(0,0,0,.65),
        0 0 30px rgba(50,200,230,.08);
}

</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="main-title">
🏭 AI VIRTUAL BEARING MANUFACTURING FACTORY
</div>

<div class="main-subtitle">
Real-Time Virtual Production • Section-Wise Inspection • AI Anomaly Detection
</div>
""",
    unsafe_allow_html=True
)

# ============================================================
# START / STOP
# ============================================================

button1, button2, space = st.columns(
    [1.4, 1.4, 5]
)

with button1:

    if st.button(
        "▶ START FACTORY",
        use_container_width=True
    ):

        st.session_state.factory_running = True

        # Immediately generate data
        record = generate_live_record()

        save_record(record)

        st.session_state.last_record = record

        st.session_state.total_produced += 1

        st.session_state.total_defects += record["Defects"]

        if record["Status"] == "WARNING":
            st.session_state.total_anomalies += 1

        st.session_state.cycle += 1

        st.rerun()

with button2:

    if st.button(
        "■ STOP FACTORY",
        use_container_width=True
    ):

        st.session_state.factory_running = False

        st.rerun()

# ============================================================
# CURRENT FACTORY STATE
# ============================================================

if st.session_state.factory_running:

    st.success(
        "🟢 FACTORY RUNNING — LIVE BEARING PRODUCTION ACTIVE"
    )

else:

    st.info(
        "⚪ FACTORY STOPPED — Press START FACTORY to begin live production."
    )

# ============================================================
# LIVE DATA GENERATION
# ============================================================

if st.session_state.factory_running:

    current_time = time.time()

    if (
        current_time -
        st.session_state.last_record_time
        >= 2
    ):

        record = generate_live_record()

        save_record(record)

        st.session_state.last_record = record

        st.session_state.total_produced += 1

        st.session_state.total_defects += record["Defects"]

        if record["Status"] == "WARNING":
            st.session_state.total_anomalies += 1

        st.session_state.cycle += 1

        st.session_state.last_record_time = current_time

# ============================================================
# LOAD LIVE DATA
# ============================================================

records = read_data()

# Keep latest 1000 records for calculations
records = records[-1000:]

# ============================================================
# CALCULATE LIVE VALUES
# ============================================================

if records:

    recent = records[-30:]

    latest = records[-1]

    warning_records = [
        r for r in recent
        if str(r["Status"]).upper() == "WARNING"
    ]

    warning_count = len(warning_records)

    average_temperature = sum(
        r["Temperature_C"]
        for r in recent
    ) / len(recent)

    average_vibration = sum(
        r["Vibration_mm_s"]
        for r in recent
    ) / len(recent)

    average_speed = sum(
        r["Speed_RPM"]
        for r in recent
    ) / len(recent)

    recent_output = sum(
        r["Output_Units"]
        for r in recent
    )

    recent_defects = sum(
        r["Defects"]
        for r in recent
    )

else:

    latest = {
        "Status": "WAITING",
        "Process_Name": "Waiting for production",
        "Temperature_C": 0,
        "Vibration_mm_s": 0,
        "Speed_RPM": 0,
        "Defects": 0
    }

    warning_count = 0
    average_temperature = 0
    average_vibration = 0
    average_speed = 0
    recent_output = 0
    recent_defects = 0

# ============================================================
# SYSTEM STATUS
# ============================================================

if not st.session_state.factory_running:

    system_status = "⚪ STOPPED"

elif latest["Status"] == "WARNING":

    system_status = "🔴 ATTENTION"

elif average_vibration >= 2.5:

    system_status = "🟠 MONITOR"

else:

    system_status = "🟢 NORMAL"

# ============================================================
# AI RECOMMENDATION
# ============================================================

if latest["Status"] == "WARNING":

    ai_message = (
        "🔴 ANOMALY DETECTED. "
        f"The bearing is currently associated with "
        f"{latest['Process_Name']}. "
        "Temperature/vibration has crossed the normal range. "
        "The bearing should be diverted to the inspection area "
        "and checked by the worker before packaging."
    )

elif average_vibration >= 2.5:

    ai_message = (
        "🟠 ELEVATED VIBRATION. "
        "AI recommends monitoring the current machine "
        "and checking bearing alignment before continuing."
    )

else:

    ai_message = (
        "🟢 PRODUCTION NORMAL. "
        "Bearing condition is healthy. "
        "The bearing can continue through the remaining sections "
        "and proceed to packaging."
    )

# ============================================================
# SYSTEM STATUS + AI
# ============================================================

st.markdown("## 🧠 System Status & AI Analytics")

status_col, ai_col = st.columns(
    [1, 2.5]
)

with status_col:

    st.markdown(
        f"""
<div class="info-card">

<div class="info-title">
SYSTEM STATUS
</div>

<div class="info-value">
{system_status}
</div>

</div>
""",
        unsafe_allow_html=True
    )

with ai_col:

    st.markdown(
        f"""
<div class="ai-card">

<b>🤖 AI ANALYTICS & RECOMMENDATION</b>

<br><br>

{ai_message}

</div>
""",
        unsafe_allow_html=True
    )

# ============================================================
# 3D VIRTUAL FACTORY
# ============================================================

st.markdown("## 🏭 Live 3D Virtual Bearing Factory")

factory_html = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

html,body{
    margin:0;
    padding:0;
    width:100%;
    height:100%;
    overflow:hidden;
    background:#050b10;
    font-family:Arial,sans-serif;
}

#factory{
    position:relative;
    width:100%;
    height:650px;
    overflow:hidden;
    border-radius:25px;
    border:2px solid #315967;
    background:
        linear-gradient(
            180deg,
            #173b48 0%,
            #102d38 45%,
            #071218 100%
        );
    box-shadow:
        0 20px 60px rgba(0,0,0,.8),
        inset 0 0 100px rgba(60,220,255,.08);
}

.ceiling-light{
    position:absolute;
    top:45px;
    width:130px;
    height:6px;
    border-radius:10px;
    background:#dfffff;
    box-shadow:
        0 0 12px #a9f5ff,
        0 0 30px #4dddf4;
}

.light1{left:6%}
.light2{left:26%}
.light3{left:46%}
.light4{left:66%}
.light5{left:86%}

.factory-heading{
    position:absolute;
    top:18px;
    left:0;
    width:100%;
    text-align:center;
    color:#86edff;
    font-size:25px;
    font-weight:900;
    letter-spacing:2px;
    text-shadow:0 0 15px #36dfff;
}

.floor{
    position:absolute;
    left:-5%;
    bottom:-90px;
    width:110%;
    height:350px;
    transform:
        perspective(700px)
        rotateX(60deg);
    transform-origin:bottom;
    background:
        repeating-linear-gradient(
            90deg,
            #314b53 0px,
            #314b53 65px,
            #20343b 66px,
            #20343b 130px
        );
}

.section{
    position:absolute;
    top:125px;
    width:130px;
    height:180px;
    border-radius:18px;
    background:
        linear-gradient(145deg,#234a57,#0b2029);
    border:2px solid #56baca;
    box-shadow:
        0 12px 30px rgba(0,0,0,.6);
    z-index:10;
}

.section.warning{
    border-color:#ff294d;
    background:
        linear-gradient(145deg,#581c27,#240b12);
    box-shadow:
        0 0 25px rgba(255,30,60,.8),
        0 0 55px rgba(255,30,60,.35);
}

.section.s1{left:2%}
.section.s2{left:18%}
.section.s3{left:34%}
.section.s4{left:50%}
.section.s5{left:66%}
.section.s6{left:82%}

.machine{
    position:absolute;
    top:48px;
    left:15px;
    width:96px;
    height:67px;
    border-radius:12px;
    background:
        linear-gradient(145deg,#7c979e,#263c44);
    border:2px solid #b1cbd0;
    box-shadow:
        inset 0 0 18px rgba(255,255,255,.15),
        0 8px 20px rgba(0,0,0,.7);
}

.machine:after{
    content:"";
    position:absolute;
    left:30px;
    top:12px;
    width:30px;
    height:30px;
    border-radius:50%;
    border:7px solid #dcecef;
    background:#172a31;
    box-shadow:0 0 14px #69e9ff;
}

.section-name{
    position:absolute;
    bottom:10px;
    width:100%;
    text-align:center;
    color:#eaffff;
    font-size:11px;
    font-weight:900;
}

.conveyor{
    position:absolute;
    top:325px;
    height:44px;
    background:
        repeating-linear-gradient(
            90deg,
            #6d858c 0px,
            #6d858c 27px,
            #192a30 28px,
            #192a30 55px
        );
    border-top:5px solid #abc1c6;
    border-bottom:5px solid #101a1f;
    box-shadow:0 10px 25px rgba(0,0,0,.7);
    z-index:5;
}

.cv1{left:2%;width:16%}
.cv2{left:18%;width:16%}
.cv3{left:34%;width:16%}
.cv4{left:50%;width:16%}
.cv5{left:66%;width:16%}
.cv6{left:82%;width:16%}

.bearing{
    position:absolute;
    width:36px;
    height:36px;
    border-radius:50%;
    z-index:40;
    border:7px solid #d9e8eb;
    background:
        radial-gradient(
            circle,
            #13252c 0 22%,
            #a9bdc2 24% 35%,
            #263d45 37% 100%
        );
    box-shadow:
        0 0 13px rgba(220,250,255,.8),
        0 6px 15px rgba(0,0,0,.7);
}

.bearing.normal{
    border-color:#6dffae;
    box-shadow:
        0 0 17px #32ff91,
        0 0 35px rgba(30,255,120,.5);
}

.bearing.bad{
    border-color:#ff294b;
    box-shadow:
        0 0 20px #ff294b,
        0 0 45px rgba(255,20,50,.8);
}

.worker{
    position:absolute;
    width:42px;
    height:82px;
    z-index:25;
    animation:
        workMove 1.6s
        infinite alternate ease-in-out;
}

.worker-head{
    position:absolute;
    left:11px;
    top:0;
    width:19px;
    height:19px;
    border-radius:50%;
    background:#f2bc8a;
    border:2px solid #d99a69;
}

.worker-body{
    position:absolute;
    left:6px;
    top:21px;
    width:30px;
    height:37px;
    border-radius:8px;
    background:#138eae;
    border:2px solid #6ee8ff;
}

.worker-leg1,
.worker-leg2{
    position:absolute;
    top:56px;
    width:7px;
    height:25px;
    border-radius:5px;
    background:#273d45;
}

.worker-leg1{left:10px}
.worker-leg2{left:25px}

.worker-arm1,
.worker-arm2{
    position:absolute;
    top:26px;
    width:7px;
    height:27px;
    border-radius:5px;
    background:#f0b681;
    transform-origin:top;
}

.worker-arm1{
    left:0;
    transform:rotate(20deg);
}

.worker-arm2{
    right:0;
    transform:rotate(-20deg);
}

@keyframes workMove{
    from{transform:translateX(-7px)}
    to{transform:translateX(7px)}
}

.box{
    position:absolute;
    bottom:90px;
    width:55px;
    height:45px;
    background:
        linear-gradient(145deg,#e6b75d,#82571e);
    border:2px solid #ffd274;
    box-shadow:0 8px 18px rgba(0,0,0,.7);
    z-index:20;
}

.box1{right:2%}
.box2{right:8%}
.box3{right:14%}

.reject-area{
    position:absolute;
    left:67%;
    bottom:28px;
    width:190px;
    height:75px;
    border:2px dashed #ff405d;
    border-radius:15px;
    background:rgba(80,5,15,.55);
    color:#ff7285;
    text-align:center;
    padding-top:16px;
    font-size:12px;
    font-weight:900;
    z-index:22;
}

.live-panel{
    position:absolute;
    right:18px;
    top:78px;
    width:205px;
    padding:15px;
    border-radius:15px;
    background:rgba(4,13,18,.94);
    border:1px solid #41606a;
    color:#dffaff;
    z-index:100;
    font-size:13px;
    box-shadow:0 8px 25px rgba(0,0,0,.5);
}

.live-title{
    color:#6eeaff;
    font-weight:900;
    margin-bottom:8px;
}

.red-flash{
    animation:flash .45s infinite alternate;
}

@keyframes flash{
    from{opacity:1}
    to{opacity:.35}
}

</style>
</head>

<body>

<div id="factory">

    <div class="floor"></div>

    <div class="ceiling-light light1"></div>
    <div class="ceiling-light light2"></div>
    <div class="ceiling-light light3"></div>
    <div class="ceiling-light light4"></div>
    <div class="ceiling-light light5"></div>

    <div class="factory-heading">
        🏭 LIVE 3D VIRTUAL BEARING FACTORY
    </div>

    <!-- SECTIONS -->

    <div class="section s1" id="section0">
        <div class="machine"></div>
        <div class="section-name">⚙️ TURNING</div>
    </div>

    <div class="section s2" id="section1">
        <div class="machine"></div>
        <div class="section-name">🔥 HEAT TREATMENT</div>
    </div>

    <div class="section s3" id="section2">
        <div class="machine"></div>
        <div class="section-name">⚙️ GRINDING & HONING</div>
    </div>

    <div class="section s4" id="section3">
        <div class="machine"></div>
        <div class="section-name">🔧 ASSEMBLY</div>
    </div>

    <div class="section s5" id="section4">
        <div class="machine"></div>
        <div class="section-name">🔍 QUALITY INSPECTION</div>
    </div>

    <div class="section s6" id="section5">
        <div class="machine"></div>
        <div class="section-name">📦 PACKAGING</div>
    </div>

    <!-- CONVEYORS -->

    <div class="conveyor cv1"></div>
    <div class="conveyor cv2"></div>
    <div class="conveyor cv3"></div>
    <div class="conveyor cv4"></div>
    <div class="conveyor cv5"></div>
    <div class="conveyor cv6"></div>

    <!-- WORKERS -->

    <div class="worker" style="left:10%;top:395px;">
        <div class="worker-head"></div>
        <div class="worker-body"></div>
        <div class="worker-arm1"></div>
        <div class="worker-arm2"></div>
        <div class="worker-leg1"></div>
        <div class="worker-leg2"></div>
    </div>

    <div class="worker" style="left:40%;top:395px;">
        <div class="worker-head"></div>
        <div class="worker-body"></div>
        <div class="worker-arm1"></div>
        <div class="worker-arm2"></div>
        <div class="worker-leg1"></div>
        <div class="worker-leg2"></div>
    </div>

    <div class="worker" style="left:69%;top:395px;">
        <div class="worker-head"></div>
        <div class="worker-body"></div>
        <div class="worker-arm1"></div>
        <div class="worker-arm2"></div>
        <div class="worker-leg1"></div>
        <div class="worker-leg2"></div>
    </div>

    <div class="worker" style="left:90%;top:395px;">
        <div class="worker-head"></div>
        <div class="worker-body"></div>
        <div class="worker-arm1"></div>
        <div class="worker-arm2"></div>
        <div class="worker-leg1"></div>
        <div class="worker-leg2"></div>
    </div>

    <!-- PACKING BOXES -->

    <div class="box box1"></div>
    <div class="box box2"></div>
    <div class="box box3"></div>

    <!-- REJECTION AREA -->

    <div class="reject-area" id="reject">
        ⚠️ ANOMALY INSPECTION<br>
        👷 WORKER AREA
    </div>

    <!-- LIVE PANEL -->

    <div class="live-panel">

        <div class="live-title">
            LIVE FACTORY
        </div>

        <div id="factoryStatus">
            🟢 PRODUCTION RUNNING
        </div>

        <br>

        <div>
            Bearings: <span id="bearingCount">0</span>
        </div>

        <div>
            Packed: <span id="packedCount">0</span>
        </div>

        <div>
            Rejected: <span id="rejectCount">0</span>
        </div>

    </div>

</div>

<script>

/* ============================================================
   FACTORY ENGINE
   ============================================================ */

const factory = document.getElementById("factory");

const sections = [
    document.getElementById("section0"),
    document.getElementById("section1"),
    document.getElementById("section2"),
    document.getElementById("section3"),
    document.getElementById("section4"),
    document.getElementById("section5")
];

const positions = [5,21,37,53,69,85];

let bearingObjects = [];

let bearingCounter = 0;
let packedCounter = 0;
let rejectedCounter = 0;

let audio = null;

/* ============================================================
   AUDIO
   ============================================================ */

function enableAudio(){

    try{

        if(!audio){

            audio =
                new (
                    window.AudioContext ||
                    window.webkitAudioContext
                )();

        }

        if(audio.state === "suspended"){
            audio.resume();
        }

    }catch(error){

        console.log(error);

    }

}

function anomalySound(){

    try{

        enableAudio();

        if(!audio){
            return;
        }

        const now =
            audio.currentTime;

        const osc =
            audio.createOscillator();

        const gain =
            audio.createGain();

        osc.type = "square";

        osc.frequency.setValueAtTime(
            850,
            now
        );

        osc.frequency.setValueAtTime(
            1050,
            now + 0.18
        );

        gain.gain.setValueAtTime(
            0.001,
            now
        );

        gain.gain.exponentialRampToValueAtTime(
            0.28,
            now + 0.03
        );

        gain.gain.exponentialRampToValueAtTime(
            0.001,
            now + 0.38
        );

        osc.connect(gain);

        gain.connect(
            audio.destination
        );

        osc.start(now);

        osc.stop(
            now + 0.4
        );

    }catch(error){

        console.log(
            "Audio:",
            error
        );

    }

}

/* ============================================================
   USER CLICK ENABLES SOUND
   ============================================================ */

factory.addEventListener(
    "click",
    function(){

        enableAudio();

    }
);

/* ============================================================
   CREATE BEARING
   ============================================================ */

function createBearing(){

    const element =
        document.createElement("div");

    const isBad =
        Math.random() < 0.18;

    element.className =
        isBad
        ? "bearing bad"
        : "bearing normal";

    element.style.left = "4%";
    element.style.top = "326px";

    factory.appendChild(
        element
    );

    const object = {

        element: element,

        section: 0,

        progress: Math.random() * 0.25,

        anomaly: isBad,

        stopped: false,

        detected: false

    };

    bearingObjects.push(
        object
    );

    bearingCounter++;

}

/* ============================================================
   UPDATE COUNTERS
   ============================================================ */

function updatePanel(){

    document.getElementById(
        "bearingCount"
    ).innerText =
        bearingCounter;

    document.getElementById(
        "packedCount"
    ).innerText =
        packedCounter;

    document.getElementById(
        "rejectCount"
    ).innerText =
        rejectedCounter;

}

/* ============================================================
   PACK NORMAL BEARING
   ============================================================ */

function packBearing(obj){

    if(obj.stopped){
        return;
    }

    obj.stopped = true;

    const element =
        obj.element;

    element.style.transition =
        "all 1.3s ease";

    element.style.left =
        "94%";

    element.style.top =
        "470px";

    element.style.transform =
        "rotate(720deg) scale(.5)";

    setTimeout(
        function(){

            element.style.left =
                "94%";

            element.style.top =
                "535px";

            element.style.transform =
                "rotate(1080deg) scale(.25)";

            element.style.opacity =
                "0";

        },
        700
    );

    setTimeout(
        function(){

            if(element.parentNode){
                element.remove();
            }

            packedCounter++;

            updatePanel();

            document.getElementById(
                "factoryStatus"
            ).innerText =
                "🟢 NORMAL BEARING PACKED";

        },
        1400
    );

}

/* ============================================================
   REJECT BAD BEARING
   ============================================================ */

function rejectBearing(obj){

    if(obj.stopped){
        return;
    }

    obj.stopped = true;

    const element =
        obj.element;

    const reject =
        document.getElementById(
            "reject"
        );

    reject.innerHTML =
        "🔴 ANOMALY DETECTED<br>👷 WORKER REMOVING";

    element.style.transition =
        "all 1s ease";

    element.style.left =
        "75%";

    element.style.top =
        "460px";

    setTimeout(
        function(){

            reject.innerHTML =
                "👷 WORKER INSPECTION<br>🔴 DEFECTIVE BEARING";

            element.style.left =
                "78%";

            element.style.top =
                "500px";

        },
        900
    );

    setTimeout(
        function(){

            reject.innerHTML =
                "❌ REJECTED<br>🔴 DEFECTIVE BEARING";

            element.style.transition =
                "all .8s ease";

            element.style.left =
                "73%";

            element.style.top =
                "570px";

            element.style.transform =
                "rotate(1080deg) scale(.35)";

            element.style.opacity =
                "0";

        },
        1900
    );

    setTimeout(
        function(){

            if(element.parentNode){
                element.remove();
            }

            rejectedCounter++;

            updatePanel();

            document.getElementById(
                "factoryStatus"
            ).innerText =
                "🔴 DEFECTIVE BEARING REJECTED";

        },
        2700
    );

}

/* ============================================================
   MOVE BEARINGS
   ============================================================ */

function moveBearing(obj){

    if(obj.stopped){
        return;
    }

    obj.progress += 0.0075;

    if(obj.progress >= 1){

        obj.progress = 0;

        obj.section++;

        /* ---------------------------------------------
           ANOMALY DETECTION
           --------------------------------------------- */

        if(
            obj.anomaly &&
            !obj.detected &&
            obj.section >= 1
        ){

            obj.detected = true;

            const current =
                sections[
                    Math.min(
                        obj.section,
                        5
                    )
                ];

            if(current){

                current.classList.add(
                    "warning"
                );

                setTimeout(
                    function(){

                        current.classList.remove(
                            "warning"
                        );

                    },
                    2200
                );

            }

            anomalySound();

            document.getElementById(
                "factoryStatus"
            ).innerText =
                "🔴 ANOMALY DETECTED";

        }

        /* ---------------------------------------------
           BAD BEARING → REJECTION
           --------------------------------------------- */

        if(
            obj.anomaly &&
            obj.section >= 4
        ){

            rejectBearing(obj);

            return;

        }

        /* ---------------------------------------------
           NORMAL BEARING → PACKAGING
           --------------------------------------------- */

        if(
            !obj.anomaly &&
            obj.section >= 5
        ){

            packBearing(obj);

            return;

        }

    }

    const currentSection =
        Math.min(
            obj.section,
            5
        );

    const nextSection =
        Math.min(
            obj.section + 1,
            5
        );

    const start =
        positions[currentSection];

    const end =
        positions[nextSection];

    const x =
        start +
        (
            end - start
        ) *
        obj.progress;

    obj.element.style.left =
        x + "%";

    obj.element.style.top =
        "326px";

}

/* ============================================================
   MAIN ANIMATION LOOP
   ============================================================ */

function animationLoop(){

    for(
        let i = 0;
        i < bearingObjects.length;
        i++
    ){

        if(
            bearingObjects[i] &&
            bearingObjects[i].element &&
            bearingObjects[i].element.parentNode
        ){

            moveBearing(
                bearingObjects[i]
            );

        }

    }

    updatePanel();

    requestAnimationFrame(
        animationLoop
    );

}

/* ============================================================
   CONTINUOUS PRODUCTION
   ============================================================ */

setInterval(
    function(){

        createBearing();

    },
    1700
);

/* ============================================================
   START WITH MULTIPLE BEARINGS
   ============================================================ */

for(
    let i = 0;
    i < 6;
    i++
){

    setTimeout(
        function(){

            createBearing();

        },
        i * 500
    );

}

/* ============================================================
   START ENGINE
   ============================================================ */

animationLoop();

</script>

</body>

</html>
"""

st.components.v1.html(
    factory_html,
    height=670,
    scrolling=False
)

# ============================================================
# LIVE PERFORMANCE
# ============================================================

st.markdown("## 📊 Live Factory Performance")

k1, k2, k3, k4, k5 = st.columns(5)

with k1:

    st.metric(
        "🏭 Production",
        st.session_state.total_produced
    )

with k2:

    st.metric(
        "🔴 Defects",
        st.session_state.total_defects
    )

with k3:

    st.metric(
        "🌡️ Temperature",
        f"{average_temperature:.1f} °C"
    )

with k4:

    st.metric(
        "📳 Vibration",
        f"{average_vibration:.2f} mm/s"
    )

with k5:

    st.metric(
        "⚙️ Machine Speed",
        f"{average_speed:.0f} RPM"
    )

# ============================================================
# OEE
# ============================================================

st.markdown("## ⚙️ Overall Equipment Effectiveness")

if recent_output > 0:

    quality_factor = (
        recent_output - recent_defects
    ) / recent_output

else:

    quality_factor = 1.0

if warning_count > 0:

    availability_factor = 0.84

else:

    availability_factor = 0.97

performance_factor = 0.94

oee = (
    availability_factor
    *
    performance_factor
    *
    quality_factor
    *
    100
)

oee = max(
    0,
    min(100, oee)
)

st.progress(
    int(oee)
)

st.write(
    f"### OEE: {oee:.1f}%"
)

# ============================================================
# ENERGY
# ============================================================

st.markdown("## ⚡ Energy Consumption")

energy = (
    4.5
    +
    (average_speed * 0.002)
    +
    (average_temperature * 0.035)
)

if warning_count > 0:
    energy += 3.5

st.metric(
    "Estimated Current Consumption",
    f"{energy:.2f} kWh"
)

if warning_count > 0:

    st.warning(
        "⚠️ Energy consumption is higher because "
        "an abnormal machine condition has been detected."
    )

else:

    st.success(
        "🟢 Energy consumption is within the normal operating range."
    )

# ============================================================
# QUALITY
# ============================================================

st.markdown("## 🔍 Quality Overview")

if recent_output > 0:

    good_percent = (
        (
            recent_output -
            recent_defects
        )
        /
        recent_output
    ) * 100

else:

    good_percent = 100

good_percent = max(
    0,
    min(100, good_percent)
)

quality_col1, quality_col2 = st.columns(2)

with quality_col1:

    st.metric(
        "🟢 Good Bearings",
        f"{good_percent:.1f}%"
    )

with quality_col2:

    st.metric(
        "🔴 Defective Bearings",
        recent_defects
    )

if recent_defects > 0:

    st.error(
        "🔴 Defective bearing detected. "
        "Worker inspection/rejection process activated."
    )

else:

    st.success(
        "🟢 All recent bearings passed quality inspection."
    )

# ============================================================
# VIBRATION ANALYSIS
# ============================================================

st.markdown("## 📈 Vibration Analysis")

if average_vibration >= 4:

    st.error(
        f"🔴 CRITICAL VIBRATION — "
        f"{average_vibration:.2f} mm/s"
    )

elif average_vibration >= 2.5:

    st.warning(
        f"🟠 ELEVATED VIBRATION — "
        f"{average_vibration:.2f} mm/s"
    )

else:

    st.success(
        f"🟢 NORMAL VIBRATION — "
        f"{average_vibration:.2f} mm/s"
    )

# ============================================================
# SECTION-WISE STATUS
# ============================================================

st.markdown("## 🏭 Section-Wise Bearing Inspection")

section_columns = st.columns(6)

for index, section in enumerate(FACTORY_SECTIONS):

    section_records = [
        r for r in records
        if r["Machine_ID"] == section["id"]
    ]

    if section_records:

        current = section_records[-1]

        temperature = current["Temperature_C"]
        vibration = current["Vibration_mm_s"]

        if current["Status"] == "WARNING":

            status = "🔴 ANOMALY"

        else:

            status = "🟢 NORMAL"

    else:

        temperature = section["temperature"]
        vibration = section["vibration"]
        status = "⚪ WAITING"

    with section_columns[index]:

        st.markdown(
            f"""
<div class="section-card">

<b>{section["short"]}</b>

<br><br>

{status}

<br><br>

🌡️ {temperature:.1f} °C

<br>

📳 {vibration:.2f} mm/s

</div>
""",
            unsafe_allow_html=True
        )

# ============================================================
# LATEST EVENT
# ============================================================

st.markdown("## 🔄 Latest Factory Event")

if records:

    latest_status = str(
        latest["Status"]
    ).upper()

    if latest_status == "WARNING":

        st.error(
            "🔴 "
            + latest["Timestamp"]
            + " | "
            + latest["Process_Name"]
            + " | ANOMALY DETECTED | "
            + "Temperature "
            + str(latest["Temperature_C"])
            + " °C | Vibration "
            + str(latest["Vibration_mm_s"])
            + " mm/s | Bearing diverted for inspection."
        )

    else:

        st.success(
            "🟢 "
            + latest["Timestamp"]
            + " | "
            + latest["Process_Name"]
            + " | NORMAL | "
            + "Temperature "
            + str(latest["Temperature_C"])
            + " °C | Vibration "
            + str(latest["Vibration_mm_s"])
            + " mm/s | Bearing continues production."
        )

else:

    st.info(
        "Waiting for live factory data..."
    )

# ============================================================
# AUTO REFRESH
# ============================================================

if st.session_state.factory_running:

    time.sleep(2)

    st.rerun()


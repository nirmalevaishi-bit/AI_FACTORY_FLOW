import streamlit as st


def render_factory_layout():
    st.markdown("### 🏭 Visual Factory Floor Layout")

    # कस्टम CSS - व्हिज्युअल मशीन बॉक्स बनवण्यासाठी
    st.markdown(
        """
        <style>
        .machine-card {
            border: 2px solid #333;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 10px;
        }
        .status-busy { background-color: #fff3cd; border-color: #ffebaa; }
        .status-overloaded { background-color: #f8d7da; border-color: #f5c6cb; }
        .status-idle { background-color: #d4edda; border-color: #c3e6cb; }
        .arrow-box {
            font-size: 28px;
            text-align: center;
            padding-top: 45px;
            color: #555;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )  # इथे दुरुस्ती केली आहे

    # ४ मशीन्सचा लेआउट आणि मधे ॲरो (Arrow)
    cols = st.columns([3, 1, 3, 1, 3, 1, 3])

    # 1. Lathe Machine
    with cols[0]:
        st.markdown(
            """
            <div class="machine-card status-busy">
                <h2>⚙️</h2>
                <h3>Lathe Machine</h3>
                <p><b>Status:</b> BUSY 🟡</p>
                <hr>
                <p>📦 Queue: <b>3 parts</b></p>
                <p>⏳ Wait: <b>5 min</b></p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # Arrow 1
    with cols[1]:
        st.markdown('<div class="arrow-box">➡️</div>', unsafe_allow_html=True)

    # 2. Grinding Machine
    with cols[2]:
        st.markdown(
            """
            <div class="machine-card status-overloaded">
                <h2>🚨</h2>
                <h3>Grinding Machine</h3>
                <p><b>Status:</b> OVERLOADED 🔴</p>
                <hr>
                <p>📦 Queue: <b>9 parts</b></p>
                <p>⏳ Wait: <b>18 min</b></p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # Arrow 2
    with cols[3]:
        st.markdown('<div class="arrow-box">➡️</div>', unsafe_allow_html=True)

    # 3. Assembly Machine
    with cols[4]:
        st.markdown(
            """
            <div class="machine-card status-idle">
                <h2>🤖</h2>
                <h3>Assembly Station</h3>
                <p><b>Status:</b> IDLE 🟢</p>
                <hr>
                <p>📦 Queue: <b>0 parts</b></p>
                <p>⏳ Wait: <b>0 min</b></p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # Arrow 3
    with cols[5]:
        st.markdown('<div class="arrow-box">➡️</div>', unsafe_allow_html=True)

    # 4. Polishing Machine
    with cols[6]:
        st.markdown(
            """
            <div class="machine-card status-busy">
                <h2>🧰</h2>
                <h3>Polishing Machine</h3>
                <p><b>Status:</b> BUSY 🟡</p>
                <hr>
                <p>📦 Queue: <b>2 parts</b></p>
                <p>⏳ Wait: <b>4 min</b></p>
            </div>
        """,
            unsafe_allow_html=True,
        )
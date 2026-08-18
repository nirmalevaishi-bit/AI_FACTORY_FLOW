import streamlit as st
import streamlit.components.v1 as components


def render_factory_layout():

    html = """
    <style>

    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        font-family: Arial, sans-serif;
    }

    .factory {
        background: #07131f;
        padding: 30px 25px 40px 25px;
        border-radius: 18px;
        color: white;
        overflow: hidden;
    }

    .factory-title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 8px;
    }

    .factory-subtitle {
        text-align: center;
        color: #b8c7d9;
        margin-bottom: 35px;
    }

    .production-line {
        position: relative;
        width: 100%;
        height: 330px;
        overflow: hidden;
    }

    /* Conveyor */

    .conveyor {
        position: absolute;
        top: 155px;
        left: 3%;
        width: 94%;
        height: 14px;
        background: #68727c;
        border-radius: 10px;
        box-shadow: 0 0 8px #444;
    }

    .conveyor::before {
        content: "";
        position: absolute;
        width: 100%;
        height: 4px;
        top: 5px;
        background: repeating-linear-gradient(
            90deg,
            #222 0px,
            #222 25px,
            transparent 25px,
            transparent 50px
        );
    }

    /* Moving product */

    .product {
        position: absolute;
        top: 130px;
        left: 2%;
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: #22a7f0;
        border: 4px solid white;
        box-shadow: 0 0 18px #22a7f0;

        animation: moveProduct 18s linear infinite;
        z-index: 10;
    }

    @keyframes moveProduct {

        0% {
            left: 2%;
        }

        12% {
            left: 15%;
        }

        25% {
            left: 28%;
        }

        38% {
            left: 41%;
        }

        51% {
            left: 54%;
        }

        64% {
            left: 67%;
        }

        77% {
            left: 78%;
        }

        90% {
            left: 88%;
        }

        100% {
            left: 96%;
        }
    }

    /* Machine */

    .machine {
        position: absolute;
        top: 45px;
        width: 125px;
        height: 105px;
        background: #172432;
        border: 3px solid #00d084;
        border-radius: 12px;
        text-align: center;
        padding: 10px;
        z-index: 5;

        box-shadow: 0 0 12px rgba(0, 208, 132, 0.25);
    }

    .machine:hover {
        transform: translateY(-5px);
        transition: 0.3s;
    }

    .machine-icon {
        font-size: 30px;
    }

    .machine-name {
        font-size: 13px;
        font-weight: bold;
        margin-top: 5px;
    }

    .machine-status {
        font-size: 11px;
        margin-top: 7px;
        color: #00e676;
    }

    /* Positions */

    .m1 { left: 3%; }

    .m2 { left: 17%; }

    .m3 { left: 31%; }

    .m4 {
        left: 45%;
        border-color: #ff1744;
        box-shadow: 0 0 18px rgba(255, 23, 68, 0.45);
        animation: bottleneckPulse 1.2s infinite;
    }

    .m5 { left: 59%; }

    .m6 { left: 73%; }

    .m7 { left: 87%; }

    @keyframes bottleneckPulse {

        0% {
            box-shadow: 0 0 8px rgba(255, 23, 68, 0.3);
        }

        50% {
            box-shadow: 0 0 25px rgba(255, 23, 68, 0.9);
        }

        100% {
            box-shadow: 0 0 8px rgba(255, 23, 68, 0.3);
        }
    }

    /* Data cards */

    .data {
        position: absolute;
        top: 190px;
        width: 125px;
        text-align: center;
        font-size: 11px;
        padding: 8px;
        border-radius: 8px;
        background: #0e1c29;
    }

    .d1 { left: 3%; }
    .d2 { left: 17%; }
    .d3 { left: 31%; }

    .d4 {
        left: 45%;
        background: #40151a;
        border: 1px solid #ff1744;
    }

    .d5 { left: 59%; }
    .d6 { left: 73%; }
    .d7 { left: 87%; }

    /* Arrows */

    .arrow {
        position: absolute;
        top: 135px;
        font-size: 30px;
        color: #00bfff;
        z-index: 2;
    }

    .a1 { left: 14%; }
    .a2 { left: 28%; }
    .a3 { left: 42%; }
    .a4 { left: 56%; }
    .a5 { left: 70%; }
    .a6 { left: 84%; }

    /* Alert */

    .alert {
        margin-top: 20px;
        padding: 15px;
        border-radius: 12px;
        background: #40151a;
        border: 2px solid #ff1744;
        text-align: center;
        animation: alertPulse 1.5s infinite;
    }

    @keyframes alertPulse {

        0% {
            opacity: 0.7;
        }

        50% {
            opacity: 1;
        }

        100% {
            opacity: 0.7;
        }
    }

    .alert-title {
        color: #ff5252;
        font-size: 18px;
        font-weight: bold;
    }

    .live {
        margin-top: 20px;
        text-align: center;
        color: #00e676;
        font-weight: bold;
    }

    </style>


    <div class="factory">

        <div class="factory-title">
            🏭 AI Virtual Bearing Factory
        </div>

        <div class="factory-subtitle">
            LIVE PRODUCTION SIMULATION
        </div>


        <div class="production-line">

            <div class="conveyor"></div>

            <!-- Moving Product -->

            <div class="product"></div>


            <!-- Machines -->

            <div class="machine m1">
                <div class="machine-icon">⚙️</div>
                <div class="machine-name">CUTTING</div>
                <div class="machine-status">🟢 RUNNING</div>
            </div>

            <div class="machine m2">
                <div class="machine-icon">⚙️</div>
                <div class="machine-name">TURNING</div>
                <div class="machine-status">🟢 RUNNING</div>
            </div>

            <div class="machine m3">
                <div class="machine-icon">🔥</div>
                <div class="machine-name">HEAT TREATMENT</div>
                <div class="machine-status">🟢 RUNNING</div>
            </div>

            <div class="machine m4">
                <div class="machine-icon">⚙️</div>
                <div class="machine-name">GRINDING</div>
                <div class="machine-status" style="color:#ff5252">
                    🔴 BOTTLENECK
                </div>
            </div>

            <div class="machine m5">
                <div class="machine-icon">🔍</div>
                <div class="machine-name">INSPECTION</div>
                <div class="machine-status">🟢 RUNNING</div>
            </div>

            <div class="machine m6">
                <div class="machine-icon">📦</div>
                <div class="machine-name">PACKAGING</div>
                <div class="machine-status">🟢 RUNNING</div>
            </div>

            <div class="machine m7">
                <div class="machine-icon">✅</div>
                <div class="machine-name">FINISHED</div>
                <div class="machine-status">🟢 READY</div>
            </div>


            <!-- Arrows -->

            <div class="arrow a1">➜</div>
            <div class="arrow a2">➜</div>
            <div class="arrow a3">➜</div>
            <div class="arrow a4">➜</div>
            <div class="arrow a5">➜</div>
            <div class="arrow a6">➜</div>


            <!-- Live Data -->

            <div class="data d1">
                Queue: 2<br>
                Time: 4 min<br>
                Temp: 45°C
            </div>

            <div class="data d2">
                Queue: 3<br>
                Time: 5 min<br>
                Temp: 48°C
            </div>

            <div class="data d3">
                Queue: 1<br>
                Time: 5 min<br>
                Temp: 62°C
            </div>

            <div class="data d4">
                Queue: 9 ⚠️<br>
                Wait: 18 min<br>
                Temp: 77°C
            </div>

            <div class="data d5">
                Queue: 2<br>
                Time: 4 min<br>
                Defects: 0
            </div>

            <div class="data d6">
                Queue: 1<br>
                Time: 3 min<br>
                Packed: 25
            </div>

            <div class="data d7">
                Completed: 24<br>
                Quality: 96%
            </div>

        </div>


        <div class="alert">

            <div class="alert-title">
                🚨 AI BOTTLENECK DETECTED
            </div>

            Grinding Machine

            <br><br>

            Queue: <b>9 parts</b>
            &nbsp;&nbsp; | &nbsp;&nbsp;
            Expected Wait: <b>18 min</b>

            <br><br>

            🤖 AI Recommendation:
            Check machine capacity and production flow.

        </div>


        <div class="live">
            ● LIVE FACTORY SIMULATION RUNNING
        </div>

    </div>
    """

    components.html(
        html,
        height=650,
        scrolling=False
    )
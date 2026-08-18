

import io
import joblib
import pandas as pd
import streamlit as st

from factory_layout import render_factory_layout


# =========================================================
# PATHS
# =========================================================

MODEL_WAIT_PATH = r"E:\AI_factory_flow\artifacts\wait_time_model.joblib"
MODEL_RECOMMEND_PATH = r"E:\AI_factory_flow\artifacts\machine_recommender_model.joblib"

DATA_PATH = r"E:\AI_factory_flow\data\processed\cleaned_factory_flow_data.csv"

# =========================================================
# FEATURES
# =========================================================

FEATURE_COLUMNS = [
    "Machine_ID",
    "Machine_Status",
    "Queue_Length",
    "Processing_Time",
    "Worker_Available",
    "Shift",
    "Material_Type",
    "Temperature",
    "Previous_Wait_Time",
    "Current_Wait_Time",
]


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Factory Flow Optimizer",
    page_icon="🏭",
    layout="wide"
)


# =========================================================
# LOAD DATASET
# =========================================================

@st.cache_data
def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


# =========================================================
# LOAD MODELS
# =========================================================

@st.cache_resource
def load_models():

    wait_model = joblib.load(MODEL_WAIT_PATH)

    recommend_model = joblib.load(MODEL_RECOMMEND_PATH)

    return wait_model, recommend_model


# =========================================================
# CSV INPUT
# =========================================================

def parse_csv_input(text: str) -> pd.DataFrame:

    if not text.strip():
        return pd.DataFrame()

    return pd.read_csv(io.StringIO(text))


# =========================================================
# VALIDATE BATCH INPUT
# =========================================================

def validate_batch_input(df: pd.DataFrame) -> pd.DataFrame:

    missing = [
        col for col in FEATURE_COLUMNS
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            "Input data is missing required columns: "
            + ", ".join(missing)
        )

    return df[FEATURE_COLUMNS]


# =========================================================
# SINGLE ROW INPUT
# =========================================================

def build_single_row_input() -> pd.DataFrame:

    machine_id = st.sidebar.selectbox(
        "Machine ID",
        [
            "Lathe_M1",
            "Grinding_M2",
            "Polishing_M3",
            "Assembly_M4"
        ]
    )

    machine_status = st.sidebar.selectbox(
        "Machine Status",
        [
            "Busy",
            "Idle",
            "Overloaded",
            "Maintenance"
        ]
    )

    queue_length = st.sidebar.number_input(
        "Queue Length",
        min_value=0,
        max_value=100,
        value=5
    )

    processing_time = st.sidebar.number_input(
        "Processing Time",
        min_value=1,
        max_value=120,
        value=20
    )

    worker_available = st.sidebar.selectbox(
        "Worker Available",
        ["Yes", "No"]
    )

    shift = st.sidebar.selectbox(
        "Shift",
        [
            "Morning",
            "Evening",
            "Night"
        ]
    )

    material_type = st.sidebar.selectbox(
        "Material Type",
        [
            "Bearing_Steel_Chrome",
            "Bearing_Stainless",
            "Ceramic_Hybrid"
        ]
    )

    temperature = st.sidebar.number_input(
        "Temperature",
        min_value=0,
        max_value=120,
        value=40
    )

    previous_wait_time = st.sidebar.number_input(
        "Previous Wait Time",
        min_value=0,
        max_value=200,
        value=10
    )

    current_wait_time = st.sidebar.number_input(
        "Current Wait Time",
        min_value=0,
        max_value=200,
        value=10
    )

    return pd.DataFrame([
        {
            "Machine_ID": machine_id,
            "Machine_Status": machine_status,
            "Queue_Length": queue_length,
            "Processing_Time": processing_time,
            "Worker_Available": worker_available,
            "Shift": shift,
            "Material_Type": material_type,
            "Temperature": temperature,
            "Previous_Wait_Time": previous_wait_time,
            "Current_Wait_Time": current_wait_time,
        }
    ])


# =========================================================
# BATCH INPUT
# =========================================================

def build_batch_input() -> pd.DataFrame:

    upload = st.sidebar.file_uploader(
        "Upload batch data (CSV)",
        type=["csv"]
    )

    paste = st.sidebar.text_area(
        "Or paste CSV data (include headers)",
        value=(
            "Machine_ID,Machine_Status,Queue_Length,"
            "Processing_Time,Worker_Available,Shift,"
            "Material_Type,Temperature,Previous_Wait_Time,"
            "Current_Wait_Time\n"
        ),
        height=120
    )

    if upload is not None:

        df = pd.read_csv(upload)

    elif (
        paste.strip()
        and len(paste.strip().splitlines()) > 1
    ):

        df = parse_csv_input(paste)

    else:

        return pd.DataFrame()

    return validate_batch_input(df)


# =========================================================
# BOTTLENECK CHARTS
# =========================================================

def show_bottleneck_charts(df: pd.DataFrame) -> None:

    st.subheader("📊 Queue / Bottleneck Charts")

    avg_queue = (
        df.groupby("Machine_ID")["Queue_Length"]
        .mean()
        .sort_values(ascending=False)
    )

    status_counts = (
        df["Machine_Status"]
        .value_counts()
    )

    busy_rate = (
        df[df["Machine_Status"] == "Busy"]
        .groupby("Machine_ID")
        .size()
        /
        df.groupby("Machine_ID").size()
    ).fillna(0).sort_values(ascending=False)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            "#### Avg queue length by machine"
        )

        st.bar_chart(avg_queue)

    with col2:

        st.markdown(
            "#### Machine status count"
        )

        st.bar_chart(status_counts)

    with col3:

        st.markdown(
            "#### Busy ratio by machine"
        )

        st.bar_chart(busy_rate)


# =========================================================
# BOTTLENECK DETECTION
# =========================================================

def detect_bottleneck(df: pd.DataFrame) -> None:

    st.subheader("🚨 Bottleneck Detection")

    bottleneck = (
        df.groupby("Machine_ID")["Queue_Length"]
        .mean()
        .sort_values(ascending=False)
    )

    if bottleneck.empty:

        st.warning(
            "No machine data available."
        )

        return

    machine_id = bottleneck.index[0]

    queue_length = bottleneck.iloc[0]

    machine_rows = df[
        df["Machine_ID"] == machine_id
    ]

    machine_data = machine_rows.iloc[-1]

    status = machine_data["Machine_Status"]

    processing_time = machine_data["Processing_Time"]

    temperature = machine_data["Temperature"]

    st.error(
        f"🚨 Bottleneck Detected: {machine_id}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Machine",
            machine_id
        )

    with col2:

        st.metric(
            "Avg Queue",
            f"{queue_length:.1f}"
        )

    with col3:

        st.metric(
            "Processing Time",
            f"{processing_time:.0f} min"
        )

    with col4:

        st.metric(
            "Temperature",
            f"{temperature:.0f} °C"
        )

    st.write(
        f"**Machine Status:** {status}"
    )


# =========================================================
# DATASET OVERVIEW
# =========================================================

def show_dataset_overview(df: pd.DataFrame) -> None:

    st.subheader("📁 Dataset Overview")

    st.write(
        "This dataset contains the factory flow "
        "information used by the AI models."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Records",
            len(df)
        )

    with col2:

        st.metric(
            "Machines",
            df["Machine_ID"].nunique()
        )

    with col3:

        st.metric(
            "Average Queue",
            f"{df['Queue_Length'].mean():.2f}"
        )

    st.markdown(
        "### Sample Records"
    )

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "#### Machine Status Distribution"
        )

        st.bar_chart(
            df["Machine_Status"].value_counts()
        )

    with col2:

        if "Recommended_Machine" in df.columns:

            st.markdown(
                "#### Recommended Machine Distribution"
            )

            st.bar_chart(
                df["Recommended_Machine"]
                .value_counts()
            )

    if st.checkbox(
        "Show Raw Dataset",
        value=False
    ):

        st.dataframe(
            df,
            use_container_width=True
        )


# =========================================================
# PREDICTION RESULTS
# =========================================================

def show_prediction_results(
    input_data: pd.DataFrame,
    wait_model,
    recommend_model
) -> None:

    try:

        predictions = input_data.copy()

        predictions[
            "Predicted_Waiting_Time"
        ] = wait_model.predict(
            input_data
        )

        predictions[
            "Recommended_Machine"
        ] = recommend_model.predict(
            input_data
        )

        st.subheader(
            "🔮 Prediction Results"
        )

        st.dataframe(
            predictions,
            use_container_width=True
        )

        predicted_wait = (
            predictions[
                "Predicted_Waiting_Time"
            ].iloc[0]
        )

        recommended_machine = (
            predictions[
                "Recommended_Machine"
            ].iloc[0]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Predicted Waiting Time",
                f"{predicted_wait:.2f} min"
            )

        with col2:

            st.metric(
                "Recommended Machine",
                str(recommended_machine)
            )

    except Exception as e:

        st.error(
            "Prediction failed."
        )

        st.exception(e)


# =========================================================
# MAIN APPLICATION
# =========================================================

def main():

    st.title("🏭 Factory Flow Optimizer")

    st.subheader("🏭 2D Virtual Factory")

    # Factory Layout
    render_factory_layout()

    # Load dataset
    df = load_dataset()

    # Load models
    wait_model, recommend_model = load_models()

    st.markdown("---")

    # Input mode
    st.sidebar.header("Input Mode")

    input_mode = st.sidebar.radio(
        "Select input mode",
        ["Single row", "Batch CSV"]
    )

    if input_mode == "Single row":

        input_data = build_single_row_input()

    else:

        input_data = build_batch_input()

    # Prediction button
    if st.sidebar.button("🚀 Run Prediction"):

        if input_data.empty:

            st.sidebar.warning(
                "Please provide input data before running prediction."
            )

        else:

            show_prediction_results(
                input_data,
                wait_model,
                recommend_model
            )

    st.markdown("---")

    # Dataset overview
    show_dataset_overview(df)

    # Bottleneck charts
    show_bottleneck_charts(df)

    # Bottleneck detection
    detect_bottleneck(df)


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    main()
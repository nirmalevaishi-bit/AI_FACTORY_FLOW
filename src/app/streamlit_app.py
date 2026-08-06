import io
import joblib
import pandas as pd
import streamlit as st

MODEL_WAIT_PATH = "artifacts/wait_time_model.joblib"
MODEL_RECOMMEND_PATH = "artifacts/machine_recommender_model.joblib"
DATA_PATH = "data/processed/cleaned_factory_flow_data.csv"
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

st.set_page_config(page_title="Factory Flow Optimizer", layout="wide")

@st.cache_data
def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_models():
    wait_model = joblib.load(MODEL_WAIT_PATH)
    recommend_model = joblib.load(MODEL_RECOMMEND_PATH)
    return wait_model, recommend_model


def parse_csv_input(text: str) -> pd.DataFrame:
    if not text.strip():
        return pd.DataFrame()
    return pd.read_csv(io.StringIO(text))


def validate_batch_input(df: pd.DataFrame) -> pd.DataFrame:
    missing = [col for col in FEATURE_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"Input data is missing required columns: {', '.join(missing)}"
        )
    return df[FEATURE_COLUMNS]


def build_single_row_input() -> pd.DataFrame:
    machine_id = st.sidebar.selectbox(
        "Machine ID",
        ["Lathe_M1", "Grinding_M2", "Polishing_M3", "Assembly_M4"],
    )
    machine_status = st.sidebar.selectbox(
        "Machine Status",
        ["Busy", "Idle", "Overloaded", "Maintenance"],
    )
    queue_length = st.sidebar.number_input("Queue Length", min_value=0, max_value=100, value=5)
    processing_time = st.sidebar.number_input("Processing Time", min_value=1, max_value=120, value=20)
    worker_available = st.sidebar.selectbox("Worker Available", ["Yes", "No"])
    shift = st.sidebar.selectbox("Shift", ["Morning", "Evening", "Night"])
    material_type = st.sidebar.selectbox(
        "Material Type",
        ["Bearing_Steel_Chrome", "Bearing_Stainless", "Ceramic_Hybrid"],
    )
    temperature = st.sidebar.number_input("Temperature", min_value=0, max_value=120, value=40)
    previous_wait_time = st.sidebar.number_input("Previous Wait Time", min_value=0, max_value=200, value=10)
    current_wait_time = st.sidebar.number_input("Current Wait Time", min_value=0, max_value=200, value=10)

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


def build_batch_input() -> pd.DataFrame:
    upload = st.sidebar.file_uploader("Upload batch data (CSV)", type=["csv"])
    paste = st.sidebar.text_area(
        "Or paste CSV data (include headers)",
        value="Machine_ID,Machine_Status,Queue_Length,Processing_Time,Worker_Available,Shift,Material_Type,Temperature,Previous_Wait_Time,Current_Wait_Time\n",
        height=120,
    )

    if upload is not None:
        df = pd.read_csv(upload)
    elif paste.strip() and len(paste.strip().splitlines()) > 1:
        df = parse_csv_input(paste)
    else:
        return pd.DataFrame()

    return validate_batch_input(df)


def show_bottleneck_charts(df: pd.DataFrame) -> None:
    st.subheader("Queue / Bottleneck Charts")

    avg_queue = df.groupby("Machine_ID")["Queue_Length"].mean().sort_values(ascending=False)
    status_counts = df["Machine_Status"].value_counts()
    busy_rate = (
        df[df["Machine_Status"] == "Busy"].groupby("Machine_ID").size()
        / df.groupby("Machine_ID").size()
    ).fillna(0).sort_values(ascending=False)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### Avg queue length by machine")
        st.bar_chart(avg_queue)
    with col2:
        st.markdown("#### Machine status count")
        st.bar_chart(status_counts)
    with col3:
        st.markdown("#### Busy ratio by machine")
        st.bar_chart(busy_rate)


def show_model_explainability(wait_model, recommend_model) -> None:
    st.subheader("Model Explainability")

    if not hasattr(wait_model, "named_steps") or not hasattr(recommend_model, "named_steps"):
        st.write("Model explainability is not available for this model format.")
        return

    preprocessor = wait_model.named_steps["preprocessor"]
    feature_names = preprocessor.get_feature_names_out(FEATURE_COLUMNS)

    wait_importances = wait_model.named_steps["regressor"].feature_importances_
    recommend_importances = recommend_model.named_steps["classifier"].feature_importances_

    wait_df = pd.DataFrame(
        {"feature": feature_names, "importance": wait_importances}
    ).sort_values("importance", ascending=False).head(10)
    recommend_df = pd.DataFrame(
        {"feature": feature_names, "importance": recommend_importances}
    ).sort_values("importance", ascending=False).head(10)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Waiting time model feature importances")
        st.bar_chart(wait_df.set_index("feature"))
    with col2:
        st.markdown("#### Machine recommendation model feature importances")
        st.bar_chart(recommend_df.set_index("feature"))


def show_dataset_overview(df: pd.DataFrame) -> None:
    st.subheader("Dataset Overview")
    st.write("This dataset is the cleaned factory flow data used to train the models.")
    st.markdown("### Sample records")
    st.dataframe(df.head(10), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Machine status distribution")
        st.bar_chart(df["Machine_Status"].value_counts())
    with col2:
        st.markdown("#### Recommended machine distribution")
        st.bar_chart(df["Recommended_Machine"].value_counts())

    st.markdown("### Bottleneck view")
    show_bottleneck_charts(df)

    if st.checkbox("Show raw dataset", value=False):
        st.dataframe(df, use_container_width=True)


def show_prediction_results(input_data: pd.DataFrame, wait_model, recommend_model) -> None:
    predictions = input_data.copy()
    predictions["Predicted_Waiting_Time"] = wait_model.predict(input_data)
    predictions["Recommended_Machine"] = recommend_model.predict(input_data)

    st.subheader("Prediction Results")
    st.write(predictions)


def main():
    st.title("Factory Flow Optimizer")
    st.write(
        "Use the trained models to estimate expected wait time and recommend the best next machine for a bearing at the factory."
    )

    df = load_dataset()
    wait_model, recommend_model = load_models()

    st.sidebar.header("Input mode")
    input_mode = st.sidebar.radio("Select input mode", ["Single row", "Batch CSV"])

    if input_mode == "Single row":
        input_data = build_single_row_input()
    else:
        input_data = build_batch_input()

    if st.sidebar.button("Run Prediction"):
        if input_data.empty:
            st.sidebar.warning("Please provide input data before running predictions.")
        else:
            show_prediction_results(input_data, wait_model, recommend_model)

    st.sidebar.markdown("---")
    st.sidebar.write("Use the controls above to evaluate single or batch factory scenarios.")

    show_dataset_overview(df)
    show_model_explainability(wait_model, recommend_model)


if __name__ == "__main__":
    main()

import os
import joblib
from pydantic import BaseModel
from fastapi import FastAPI
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "ai",
    "bottleneck_model.pkl"
)

model = joblib.load(MODEL_PATH)

print("AI Bottleneck Model Loaded Successfully!")
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "ai",
    "bottleneck_model.pkl"
)

model = joblib.load(MODEL_PATH)

print("Bottleneck AI model loaded successfully!")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset
file_path = "../../data/processed/final_factory_data.csv"
df = pd.read_csv(file_path)


@app.get("/")
def home():
    return {
        "message": "AI Virtual Smart Factory is running!"
    }


@app.get("/machines")
def get_machines():

    machines = []

    for machine in df["Machine_ID"].unique():

        machine_data = df[df["Machine_ID"] == machine].iloc[0]

        machines.append({
            "machine_id": str(machine_data["Machine_ID"]),
            "status": str(machine_data["Machine_Status"]),
            "temperature": float(machine_data["Temperature"]),
            "load": int(machine_data["Machine_Load"]),
            "queue": int(machine_data["Queue_Length"]),
            "processing_time": float(machine_data["Processing_Time"]),
            "bottleneck": int(machine_data["Bottleneck_Flag"]),
            "delay": str(machine_data["Delay_Level"])
        })

    return machines
class BottleneckInput(BaseModel):
    Queue_Length: float
    Processing_Time: float
    Temperature: float
    Previous_Wait_Time: float
    Current_Wait_Time: float
    Machine_Load: float


@app.post("/predict-bottleneck")
def predict_bottleneck(data: BottleneckInput):

    values = [[
        data.Queue_Length,
        data.Processing_Time,
        data.Temperature,
        data.Previous_Wait_Time,
        data.Current_Wait_Time,
        data.Machine_Load
    ]]

    prediction = model.predict(values)[0]

    if int(prediction) == 1:
        result = "Bottleneck"
        recommendation = (
            "Check machine capacity, reduce queue "
            "and consider shifting workload."
        )
    else:
        result = "Normal"
        recommendation = "Machine flow is normal."

    return {
        "prediction": int(prediction),
        "status": result,
        "recommendation": recommendation
    }
from pydantic import BaseModel


class BottleneckInput(BaseModel):
    Queue_Length: float
    Processing_Time: float
    Temperature: float
    Previous_Wait_Time: float
    Current_Wait_Time: float
    Machine_Load: float


@app.post("/predict-bottleneck")
def predict_bottleneck(data: BottleneckInput):

    values = [[
        data.Queue_Length,
        data.Processing_Time,
        data.Temperature,
        data.Previous_Wait_Time,
        data.Current_Wait_Time,
        data.Machine_Load
    ]]

    prediction = int(model.predict(values)[0])

    if prediction == 1:

        status = "Bottleneck"

        recommendation = (
            "Check machine capacity, reduce queue "
            "and consider shifting workload."
        )

    else:

        status = "Normal"

        recommendation = (
            "Machine flow is normal."
        )

    return {
        "prediction": prediction,
        "status": status,
        "recommendation": recommendation
    }
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import joblib


# =========================
# 1. Load Dataset
# =========================

DATA_PATH = "../../data/processed/final_factory_data.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded")
print("Rows:", len(df))


# =========================
# 2. Select Features
# =========================

features = [
    "Queue_Length",
    "Processing_Time",
    "Temperature",
    "Previous_Wait_Time",
    "Current_Wait_Time",
    "Machine_Load"
]

target = "Bottleneck_Flag"


X = df[features]
y = df[target]


# =========================
# 3. Train/Test Split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# =========================
# 4. Random Forest
# =========================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)


# =========================
# 5. Prediction
# =========================

y_pred = model.predict(X_test)


# =========================
# 6. Evaluation
# =========================

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# =========================
# 7. Save Model
# =========================

joblib.dump(
    model,
    "bottleneck_model.pkl"
)

print("\nModel saved successfully!")
print("File: bottleneck_model.pkl")
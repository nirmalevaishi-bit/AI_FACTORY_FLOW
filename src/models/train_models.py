import os
import numpy as np
import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    recall_score,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA_PATH = os.path.join("data", "processed", "cleaned_factory_flow_data.csv")
ARTIFACT_DIR = "artifacts"

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
CATEGORICAL_COLUMNS = [
    "Machine_ID",
    "Machine_Status",
    "Worker_Available",
    "Shift",
    "Material_Type",
]
NUMERIC_COLUMNS = [
    "Queue_Length",
    "Processing_Time",
    "Temperature",
    "Previous_Wait_Time",
    "Current_Wait_Time",
]

REGRESSION_TARGET = "Expected_Waiting_Time"
CLASSIFICATION_TARGET = "Recommended_Machine"


def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Cleaned dataset not found: {path}. Run scripts/preprocessing.py first."
        )
    return pd.read_csv(path)


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_COLUMNS,
            )
        ],
        remainder="passthrough",
    )


def build_regression_pipeline(preprocessor: ColumnTransformer) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
            ),
        ]
    )


def build_classification_pipeline(preprocessor: ColumnTransformer) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
            ),
        ]
    )


def evaluate_regression(y_true, y_pred) -> None:
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    print("\nRegression evaluation:")
    print(f"  MAE : {mae:.3f}")
    print(f"  RMSE: {rmse:.3f}")
    print(f"  R2  : {r2:.3f}")


def evaluate_classification(y_true, y_pred) -> None:
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average="macro", zero_division=0)
    recall = recall_score(y_true, y_pred, average="macro", zero_division=0)
    f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)

    print("\nClassification evaluation:")
    print(f"  Accuracy : {accuracy:.3f}")
    print(f"  Precision: {precision:.3f}")
    print(f"  Recall   : {recall:.3f}")
    print(f"  F1 score : {f1:.3f}")
    print("\nClassification report:")
    print(classification_report(y_true, y_pred, zero_division=0))
    print("Confusion matrix:")
    print(confusion_matrix(y_true, y_pred))


def save_pipeline(pipeline: Pipeline, name: str) -> None:
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    path = os.path.join(ARTIFACT_DIR, name)
    joblib.dump(pipeline, path)
    print(f"Saved model pipeline to: {path}")


def main() -> None:
    df = load_data(DATA_PATH)
    print("Loaded data shape:", df.shape)
    print(df[FEATURE_COLUMNS + [REGRESSION_TARGET, CLASSIFICATION_TARGET]].head())

    X = df[FEATURE_COLUMNS]
    y_reg = df[REGRESSION_TARGET]
    y_clf = df[CLASSIFICATION_TARGET]

    X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = train_test_split(
        X,
        y_reg,
        y_clf,
        test_size=0.2,
        random_state=42,
        stratify=y_clf,
    )

    preprocessor = build_preprocessor()
    reg_pipeline = build_regression_pipeline(preprocessor)
    clf_pipeline = build_classification_pipeline(preprocessor)

    print("\nTraining regression model...")
    reg_pipeline.fit(X_train, y_reg_train)

    print("Training classification model...")
    clf_pipeline.fit(X_train, y_clf_train)

    y_reg_pred = reg_pipeline.predict(X_test)
    y_clf_pred = clf_pipeline.predict(X_test)

    evaluate_regression(y_reg_test, y_reg_pred)
    evaluate_classification(y_clf_test, y_clf_pred)

    save_pipeline(reg_pipeline, "wait_time_model.joblib")
    save_pipeline(clf_pipeline, "machine_recommender_model.joblib")

    print("\nTraining complete.")


if __name__ == "__main__":
    main()

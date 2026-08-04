# AI Model Planning

## Problem Statement

The objective of this project is to optimize the production flow in a bearing manufacturing factory by using Machine Learning.

The system will:
- Predict the expected waiting time for each bearing.
- Recommend the best next machine to reduce bottlenecks and improve production efficiency.

---

# Model 1: Waiting Time Prediction

## Model Type
Regression

## Algorithm
Random Forest Regressor

## Purpose
Predict the expected waiting time of a bearing before processing.

## Input Features
- Machine_ID
- Machine_Name
- Machine_Status
- Queue_Length
- Processing_Time
- Worker_Available
- Shift
- Temperature
- Previous_Wait_Time
- Current_Wait_Time

## Target Variable
Expected_Waiting_Time

---

# Model 2: Machine Recommendation

## Model Type
Classification

## Algorithm
Random Forest Classifier

## Purpose
Recommend the best next machine for the bearing based on the current factory conditions.

## Input Features
- Machine_Status
- Queue_Length
- Processing_Time
- Worker_Available
- Shift
- Temperature
- Current_Machine
- Available_Machines

## Target Variable
Recommended_Machine

---

# Dataset Split

- Training Data : 80%
- Testing Data : 20%

---

# Evaluation Metrics

## Regression Model

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

## Classification Model

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

---

# Machine Learning Workflow

Factory Dataset
        ↓
Data Preprocessing
        ↓
Feature Engineering
        ↓
Train-Test Split
        ↓
Random Forest Regressor
        ↓
Waiting Time Prediction
        ↓
Random Forest Classifier
        ↓
Machine Recommendation
        ↓
Streamlit Dashboard
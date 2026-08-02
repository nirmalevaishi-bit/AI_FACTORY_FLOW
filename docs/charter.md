# Project Charter: AI-Powered Factory Flow & Queue Optimizer for Bearing Manufacturing

---

### 3. Core Problem Statement

* **What it says:** *In bearing manufacturing factories, production slows down because materials wait too long between machines, queues become overloaded, and managers cannot identify bottlenecks until delays occur*.


* **Explanation:**
* Imagine a factory making **bearings** (the metal rolling parts used in wheels, engines, and machines).
* Even if individual machines are working perfectly fine, production often slows to a crawl because parts pile up in long lines (queues) waiting for their turn at the next machine.
* Some machines get overloaded with too much work while others sit completely empty.
* **The main issue:** Factory managers are usually blind to these problems and only notice a bottleneck *after* a delay has already ruined their schedule.


## 1. Project Overview & Background

Bearing manufacturing plants involve complex, multi-stage production lines (such as Lathe machining, Grinding, Polishing, and Assembly). Inefficient queue management, unexpected machine states, and variable processing times often lead to severe bottlenecks, prolonged wait times, and underutilized workers.

This project, **AI Factory Flow**, implements an end-to-end MLOps pipeline and web application designed to model, analyze, and optimize manufacturing workflows. By leveraging synthetic data generation, structured preprocessing, and machine learning models, the system predicts and monitors queue dynamics to streamline factory throughput.

---

## 2. Project Objectives

* **Automated Data Generation:** Generate realistic, reproducible synthetic factory event datasets modeling 4 specific production machines (`Lathe_M1`, `Grinding_M2`, `Polishing_M3`, `Assembly_M4`) under varying operational states.
* **Pipeline Modularity:** Build a clean, decoupled data pipeline separating raw storage (`data/raw/`), processed features (`data/processed/`), and trained model artifacts (`artifacts/`).
* **Predictive Machine Learning:** Train robust classification and regression models (utilizing algorithms like Random Forest) to evaluate factory flow metrics and machine wait times.
* **Interactive Visualization:** Deploy a user-friendly web interface (via Streamlit) to visualize real-time factory flow analytics and model predictions.

---

## 3. Project Scope

### In-Scope

* Development of a custom Python script for generating 5,000+ records of synthetic factory operational metrics (machine status, queue lengths, temperatures, shift details, and wait times).
* Implementation of data cleaning, preprocessing, and feature engineering scripts (`src/data/make_dataset.py`).
* Training, evaluation, and serialization of machine learning models (`src/models/train_model.py`).
* Version control integration via Git and GitHub.
* Local deployment of an interactive dashboard app.

### Out-of-Scope

* Direct physical integration with live industrial IoT (IIoT) sensors or programmable logic controllers (PLCs) in a live manufacturing plant (simulated data is used instead).
* Enterprise cloud infrastructure setup (deployment is targeted locally or via community cloud tiers).

---

## 4. Stakeholders & Team

* **Project Lead / Developer:** [Your Name / Student Name]
* **Academic Supervisor / Guide:** Sir / Project Review Committee
* **End Users:** Factory Floor Managers, Operations Supervisors, and Industrial Engineers

---

## 5. High-Level Requirements

### Technical Requirements

* **Language:** Python (v3.8 or higher)
* **Core Libraries:** Pandas, NumPy, Scikit-Learn, Streamlit, Matplotlib, Seaborn
* **Environment Management:** Python `venv` virtual environment with locked dependency tracking (`requirements.txt`)

### Functional Requirements

* The system must successfully ingest raw CSV data from `data/raw/factory_flow_data.csv`.
* The ML pipeline must serialize trained model weights into the `artifacts/` folder.
* The web app must allow users to interact with model predictions dynamically.

---

## 6. Milestones & Timeline

1. **Phase 1: Environment Setup & Data Engineering** *(Completed)* — Repository structure, virtual environment configuration, Git tracking, and raw synthetic dataset generation.
2. **Phase 2: Data Preprocessing & Model Training** *(In Progress)* — Cleaning dataset features and training Random Forest classifiers/regressors.
3. **Phase 3: Application Development & Documentation** — Building the Streamlit web dashboard and finalizing technical documentation (`charter.md`, `decision_log.md`, `research_log.md`).
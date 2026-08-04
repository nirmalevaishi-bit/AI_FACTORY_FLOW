# Decision Log: AI-Powered Factory Flow & Queue Optimizer

This decision log records the architectural, technical, and tool-selection decisions made throughout the development of the **AI Factory Flow** project. Each entry details the decision context, alternatives considered, and the rationale behind the final choice.

---

## Decision 1: Use of Synthetic Data Generation over factory  Data

* **Date:** August 2026
* **Status:** Accepted
* **Context:** Real-time operational data from physical industrial dataset or PLCs across multi-stage bearing factories (`Lathe_M1`, `Grinding_M2`, `Polishing_M3`, `Assembly_M4`) was unavailable for immediate  integration.
* **Alternatives Considered:**
1. Scraping public industrial datasets (often lack specific multi-machine queue metrics).
2. Building a custom Python script using `numpy` and `pandas` to generate realistic synthetic factory event logs.


* **Decision:** We chose to build a **custom synthetic data generator script** (`scripts/generate_large_dataset.py`).
* **Rationale:** Generating synthetic data allowed us to control feature distributions (such as queue lengths, machine statuses, and shift anomalies) specifically tailored to bearing manufacturing workflows while ensuring full reproducibility via fixed random seeding (`np.random.seed(42)`).

---

## Decision 2: Choosing Python as the Core Programming Language

* **Date:** August 2026
* **Status:** Accepted
* **Context:** The project requires heavy data manipulation, machine learning modeling, and rapid web application prototyping.
* **Alternatives Considered:** R, Java, or C++.
* **Decision:** **Python** was chosen as the sole programming language.
* **Rationale:** Python offers an unmatched ecosystem for data science and MLOps, including industry-standard libraries like `pandas`, `numpy`, `scikit-learn`, and `streamlit`.

---

## Decision 3: Selecting Random Forest for Model Training

* **Date:** August 2026
* **Status:** Accepted
* **Context:** We need a robust machine learning model capable of handling tabular operational data (numerical and categorical mixes like machine status, wait times, and temperatures) to predict factory flow efficiency and bottlenecks.
* **Alternatives Considered:** Logistic Regression, Support Vector Machines (SVM), and Deep Learning (Neural Networks).
* **Decision:** **Random Forest** (ensemble tree-based learning).
* **Rationale:**
* Random Forest handles non-linear relationships and interactions between features (e.g., how temperature combined with queue length affects processing time) exceptionally well.
* It requires minimal data normalization compared to SVMs or Neural Networks.
* It is less prone to overfitting on medium-sized tabular datasets and provides built-in feature importance metrics for explainability.



---

## Decision 4: Choosing Streamlit for Web Application Deployment

* **Date:** August 2026
* **Status:** Accepted
* **Context:** The project requires an interactive web dashboard for factory supervisors and engineers to view analytics and interact with model predictions.
* **Alternatives Considered:** Full-stack web frameworks (Flask + HTML/CSS/JS) or enterprise dashboards (Dash/Django).
* **Decision:** **Streamlit**.
* **Rationale:** Streamlit allows data scientists to build and deploy interactive web applications entirely in pure Python with minimal boilerplate code, making it ideal for rapid prototyping, local demonstration, and cloud deployment.

---

## Decision 5: Modular Project Directory Structure

* **Date:** August 2026
* **Status:** Accepted
* **Context:** As the codebase grows (data scripts, model training, web apps, configs), flat directory structures quickly become unmaintainable.
* **Decision:** Adopt a modular MLOps directory structure separating `data/` (raw/processed), `src/` (data cleaning, modeling), `artifacts/` (saved models), `scripts/`, and `docs/`.
* **Rationale:** Ensures clean separation of concerns, improves code maintainability, and aligns with standard software engineering and MLOps best practices.
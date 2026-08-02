

### MY RESEARCH LOG :

---

### Breakdown of Research Log Entry 001

* **Date:** `2026-03-05`
* **What it means:** The exact calendar day your team performed this technical research.


* **Research Question:** *What is the most effective machine learning algorithm for predicting tabular waiting times and routing recommendations in factory flows?*
* **Explanation:** Your project deals with tabular data (rows and columns like queue length, temperature, and machine status). You needed to figure out which AI algorithm would do the best job at predicting how long a bearing part will wait in line and which machine it should go to next.



* **Exact Query Used:** *"Random Forest Regressor vs XGBoost for manufacturing queue time prediction"*
* **Explanation:** This shows the exact words your team searched online or in technical libraries to compare two popular machine learning tools (Random Forest and XGBoost).


* **Source/Reference:** *Scikit-learn official documentation and industrial production literature.*
* **Explanation:** The information and comparison came from official, trusted machine learning guides and manufacturing research papers.




* **Findings:** Random Forest handles tabular features robustly without extensive hyperparameter tuning, making it ideal for a 4-week student MVP timeline.
* **Explanation:** While algorithms like XGBoost are powerful, Random Forest works reliably right out of the box with very little tuning. This makes it the safer, faster choice for your team since you only have a 4-week window to build your Minimum Viable Product (MVP).




* **Project Action:** Selected Random Forest Regressor and Classifier as primary models.

Based on the research findings, your team officially chose **Random Forest Regressor** (to predict numerical waiting times) and **Random Forest Classifier** (to choose the best next machine) as the core AI models for your factory optimizer.



### MY RESERCH LINKS :

* **Scikit-Learn Documentation (Model Framework):** [Scikit-Learn Random Forest Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html) — Used for implementing the tabular regression and classification models.

* **Industrial ML Open-Source Reference:** [GitHub: ML-For-Flow-Prediction-Analytics](https://github.com/pralinkhaira/ML-For-Flow-Prediction-Analytics) — An open-source project repository demonstrating multi-stage manufacturing flow prediction and model comparison (including Random Forest and XGBoost).

* **Industrial Datasets Hub:** [Awesome Industrial Datasets GitHub Repository](https://github.com/jonathanwvd/awesome-industrial-datasets) — A curated index of manufacturing and factory datasets used for predictive analytics and process optimization.
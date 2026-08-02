**Architectural Decision Record (ADR-001)** :

---

### What is an Architectural Decision Record (ADR)?

An ADR is a short, formal document used in engineering projects to record an important technical choice. Instead of just picking a tool randomly, your team writes down *why* you chose it, the problem it solves, and what benefits it brings.

---

### Breakdown of ADR-001: Selection of Streamlit for Dashboard UI

* **Status: Accepted**

* **What it means:** Your team has officially agreed on this choice, and it is locked in as part of your project design.




* **Context:** *We need a rapid, interactive dashboard frontend to visualize factory machine layouts, queue charts, and AI recommendations without building a complex full-stack web app*.


* **Explanation:** Your AI model needs a user interface (frontend) so that factory managers can actually look at the data, see machine statuses, and read AI recommendations. Normally, building a web app requires complex tools like HTML, CSS, JavaScript, and backend frameworks. Since your team only has 4 weeks, you need something much faster and easier.




* **Decision:** *Use Streamlit for the user interface*.


* **Explanation:** You decided to use **Streamlit**, which is a Python library. It allows you to build interactive web dashboards entirely using Python code, eliminating the need to learn complicated web development languages.




* **Consequences:** *Enables fast Python-based integration and local deployment within our 4-week timeline*.


* **Explanation:** Because Streamlit is built for Python, it connects directly to your machine learning models very easily. This ensures your team can successfully build, test, and run the dashboard locally on your computers within your strict 1-month project deadline.
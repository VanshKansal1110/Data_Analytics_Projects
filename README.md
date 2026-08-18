# Data Analytics Projects

A collection of end-to-end data analytics projects — exploratory data analysis, statistical
testing, machine learning, and interactive dashboards — built while studying data analytics.

Each project lives in its own folder with its own detailed README, notebooks, source code,
and reports. This root README gives a quick overview of everything in one place; click into
any project folder for the full write-up.

---

## Projects

### [Project 01 — 6G Network Impact on Manufacturing Efficiency](./Project_01__6G_Impact_On_Manufacturing)
**Domain:** Smart manufacturing / telecom infrastructure
**Techniques:** EDA, correlation analysis, chi-square testing, Random Forest classification, custom KPI design, Streamlit dashboard
**Summary:** Investigated whether 6G network performance (latency, packet loss) drives manufacturing efficiency in a smart factory, using 100,000 machine telemetry readings. Found no statistically significant relationship across five independent methods, with strong evidence the dataset was synthetically generated — a well-documented negative result including a caught-and-corrected data leakage issue.
**Stack:** Python, Pandas, Scikit-learn, SciPy, Streamlit, Seaborn/Matplotlib

### [Project 02 — Customer Segmentation & Churn Pattern Analytics](./Project_02__Bank_Churn_Segmentation)
**Domain:** Retail banking / customer retention
**Techniques:** EDA, customer segmentation, chi-square testing, interaction analysis, revenue-at-risk quantification, Random Forest classification, custom KPI design, interactive Streamlit dashboard
**Summary:** Identified which customer segments carry the highest churn risk across 10,000 European bank customers. Found strong, statistically significant churn drivers (age, geography, gender, balance), with the highest-risk compound profile being German women aged 46-60 (60%+ churn). A Random Forest model independently confirmed the findings at 85% accuracy.
**Stack:** Python, Pandas, Scikit-learn, SciPy, Streamlit, Seaborn/Matplotlib
<!-- Add new projects below this line, following the same format -->

<!--
### [Project 0X — Project Title](./Project_0X__Folder_Name)
**Domain:** 
**Techniques:** 
**Summary:** 
**Stack:** 
-->

---

## Skills Demonstrated Across Projects

- Exploratory data analysis (data quality checks, outlier detection, distribution analysis)
- Statistical hypothesis testing (correlation, chi-square, significance testing)
- Machine learning (classification, feature importance, data leakage detection)
- Interactive dashboard development (Streamlit)
- Version control and structured, incremental Git workflows
- Technical and executive-level report writing

## Repository Structure

```
Data_Analytics_Projects/
├── README.md                          # This file — overview of all projects
├── Project_01__6G_Impact_On_Manufacturing/
│   ├── README.md                      # Full project-specific documentation
│   ├── data/
│   ├── notebooks/
│   ├── src/
│   └── reports/
│   ├── requirements.txt
│   ├── streamlit_app.py
|
├── Project_02__Bank_Churn_Segmentation/
│   ├── README.md                      # Full project-specific documentation
│   ├── data/
│   ├── notebooks/
│   ├── src/
│   └── reports/
│   ├── requirements.txt
│   ├── streamlit_app.py
├── Project_03__.../                   # Future projects follow the same structure
└── ...
```

## Setup

Each project has its own `requirements.txt`. To run a specific project:

```bash
cd Project_0X__ProjectName
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

*Maintained as part of ongoing data analytics coursework and independent practice.*

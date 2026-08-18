# Customer Segmentation & Churn Pattern Analytics in European Banking

**Client brief:** Unified Mentor × European Central Bank
**Goal:** Identify which customer segments carry the highest churn risk, quantify their financial impact, and provide targeted retention recommendations — rather than treating churn as a single, generic rate.

## Problem Statement

Banks track overall churn but lack granular insight into which customer groups are most likely to leave, how churn differs by geography, age, and financial profile, and whether it concentrates among high-value or low-value customers. Without this, retention strategy stays generic and reactive.

## Dataset

`data/raw/European_Bank.csv` — 10,000 customer records, no missing values, no duplicates.

| Column | Description |
|---|---|
| CustomerId, Surname | Identifiers — excluded from analysis |
| CreditScore | Customer creditworthiness |
| Geography | France, Spain, Germany |
| Gender, Age | Demographics |
| Tenure | Years with the bank |
| Balance | Account balance |
| NumOfProducts | Number of bank products held |
| HasCrCard, IsActiveMember | Engagement indicators |
| EstimatedSalary | Estimated annual salary |
| Exited | Churn indicator (target) — 20.37% churn rate |

## Repo Structure

```
Project_02__Bank_Churn_Segmentation/
├── data/
│   └── raw/              # Original CSV, never edited (Already Cleaned/feature-engineered version)

├── notebooks/
│   ├── 01_eda.ipynb                # Data quality, segmentation, churn analysis, KPIs
│   └── 02_churn_prediction.ipynb   # Random Forest classifier
├── src/
│   └── kpi.py                      # 5 KPI functions, reused in notebook and dashboard
├── reports/
│   ├── research_paper.md
│   └── executive_summary.md
├── streamlit_app.py                # Dashboard (root-level — required for deployment)
├── requirements.txt
└── README.md
```

**Note:** `streamlit_app.py` sits at the project root (not in a subfolder) so that Streamlit Community Cloud's deployment process finds `requirements.txt` correctly — a lesson learned from Project 1's initial deployment failure.

## Methodology

1. **Data validation** — nulls, duplicates, identifier verification, sample-size checks before trusting extreme percentages.
2. **Segmentation** — Age, Credit Score, Tenure, and Balance bands built per brief specification.
3. **Churn distribution analysis** — segment-wise churn rates, chi-square significance testing.
4. **Interaction analysis** — Geography × Age, Gender × Age/Geography.
5. **High-value customer analysis** — revenue-at-risk quantification.
6. **KPIs** — Overall Churn Rate, Segment Churn Rate, High-Value Churn Ratio, Geographic Risk Index, Engagement Drop Indicator.
7. **Predictive modeling** — Random Forest classifier, evaluated with per-class recall given class imbalance.

## Key Findings

- **Age is the dominant churn driver** — peaks at 51% for the 46-60 band (χ²=1242, p<0.001).
- **Germany churns at ~2x the rate of France/Spain** (32.4% vs ~16%), consistently across every age group.
- **The highest-risk compound profile**: German women aged 46-60, with churn exceeding 60%.
- **Churned customers hold 25% more balance on average** — churn's financial impact (24.3% of balance) exceeds its headcount impact (20.4%).
- **Inactive members churn at nearly 2x the rate of active members** — the most directly actionable finding.
- **Tenure shows no significant relationship to churn** (p=0.253); Credit Score shows only a marginal effect.
- A Random Forest classifier achieved 85% accuracy / 61% recall on churned customers, independently confirming the segmentation findings.

## Status

- [x] EDA and data quality checks
- [x] Segmentation construction
- [x] Churn distribution and significance testing
- [x] Interaction and high-value customer analysis
- [x] KPIs
- [x] Predictive model
- [x] Streamlit dashboard
- [x] Research paper
- [x] Executive summary

## Setup

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_eda.ipynb
streamlit run streamlit_app.py
```
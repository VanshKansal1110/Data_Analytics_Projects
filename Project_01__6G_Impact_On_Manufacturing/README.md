# Impact of 6G Network Performance on Manufacturing Efficiency in Smart Factories

**Client brief:** Unified Mentor × Thales Group
**Goal:** Determine how much network performance (latency, packet loss) — independent of
mechanical health (temperature, vibration, power) — drives manufacturing efficiency in a
6G-enabled smart factory, and quantify it for stakeholders.

## Problem Statement

Manufacturers can't currently tell whether efficiency drops come from network issues or
packet loss, how much latency variation is tolerable before quality degrades, or which
efficiency levels are most sensitive to network instability. This project answers those
three questions using 100,000 rows of per-minute machine telemetry from 50 machines.

## Dataset

`data/raw/Thales_Group_Manufacturing.csv` — 100,000 rows, 14 columns, no missing values.

| Column | Description |
|---|---|
| Date, Timestamp | When the reading was captured |
| Machine_ID | 1 of 50 machines |
| Operation_Mode | Idle / Active / Maintenance |
| Temperature_C, Vibration_Hz, Power_Consumption_kW | Mechanical health signals |
| Network_Latency_ms, Packet_Loss_% | 6G network performance signals |
| Quality_Control_Defect_Rate_%, Production_Speed_units_per_hr, Error_Rate_% | Output/quality signals |
| Predictive_Maintenance_Score | AI-derived maintenance readiness |
| Efficiency_Status | Target label: Low / Medium / High |

**Known data characteristic:** `Efficiency_Status` is imbalanced — Low 77.8%, Medium 19.2%,
High 3.0%. This is called out explicitly in the analysis rather than glossed over, since it
affects how any model results should be read (accuracy alone would be misleading).

## Repo Structure

```
thales-6g-manufacturing/
├── data/
│   ├── raw/              # Original CSV, never edited (Already Cleaned/feature-engineered version)
├── notebooks/
│   ├── 01_eda.ipynb              # Distributions, network quality bands
│   ├── 02_statistical_analysis.ipynb  # Chi-square, correlations
│   ├── 03_kpi_modeling.ipynb     # Custom KPIs + classifier
├── src/
│   └── kpi.py                 # Reusable KPI calculation functions
├── app/
│   └── streamlit_app.py       # Dashboard (3 modules per brief)
├── reports/
│   ├── research_paper.md      # Full write-up
│   └── executive_summary.md   # 2-page stakeholder version
├── assets/                    # Saved chart images for the paper
├── requirements.txt
└── README.md
```

## Methodology (mapped to brief)

1. **Network Performance Profiling** → `01_eda.ipynb`: latency/packet-loss distributions,
   tertile-based Low/Medium/High network quality bands.
2. **Network vs Efficiency Analysis** → `02_statistical_analysis.ipynb`: cross-tabs of
   Efficiency_Status × network band, chi-square test for association.
3. **Latency & Packet Loss Impact Diagnostics** → same notebook: correlation of latency/packet
   loss against production speed, defect rate, error rate — reported alongside mechanical-variable
   correlations for comparison.
4. **Operation Mode Interaction** → same notebook: network impact split by Idle/Active/Maintenance.
5. **KPIs + quantified impact** → `03_kpi_modeling.ipynb`: the four KPIs below, plus a classifier
   (Random Forest) whose feature importances give a defensible answer to "how much does network
   performance matter, relative to everything else."

## KPI Definitions

| KPI | Definition (as implemented in `src/kpi.py`) |
|---|---|
| Network Stability Index | Composite 0–100 score combining normalized latency + packet loss (lower = more stable) |
| Latency Sensitivity Score | Change in mean Production_Speed per 1ms increase in latency, within each network band |
| Packet Loss Impact Ratio | % change in Defect_Rate / Error_Rate between low- and high-packet-loss periods |
| Network-Efficiency Correlation | Point (latency/packet-loss threshold) where P(Efficiency = Low) crosses 50% |

## Status

- [x] EDA
- [x] Statistical analysis (correlation, chi-square overall + per operation mode)
- [x] KPIs + model (data leakage identified and corrected)
- [x] Streamlit dashboard
- [x] Research paper
- [x] Executive summary

## Key Finding

Across five independent methods (correlation, chi-square, per-mode chi-square, leak-checked
classification, and custom KPIs), this analysis found **no statistically significant
relationship** between network performance and manufacturing efficiency in this dataset.
Strong structural evidence (zero outliers, uniformly near-zero correlations across *all*
variable pairs, nearly equal classifier feature importances) suggests the dataset is
synthetically generated with independently randomized columns. See `reports/research_paper.md`
for full methodology and `reports/executive_summary.md` for a stakeholder-facing summary.

## Setup

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_eda.ipynb   # for analysis
streamlit run streamlit_app.py        # for the dashboard
```

# Impact of 6G Network Performance on Manufacturing Efficiency in Smart Factories

**Prepared for:** Thales Group (via Unified Mentor)
**Dataset:** Thales_Group_Manufacturing.csv — 100,000 rows, 50 machines, 14 fields

---

## Abstract

This study examines whether 6G network performance — specifically latency and packet loss — drives manufacturing efficiency in a simulated smart factory environment, using 100,000 machine telemetry readings across 50 machines. Using correlation analysis, chi-square tests of independence (overall and by operation mode), a Random Forest classifier, and four custom network-performance KPIs, we find no statistically significant relationship between network conditions and manufacturing efficiency in this dataset. This result is consistent across all five independent methods, suggesting either that the dataset does not capture a genuine causal relationship (most likely due to synthetic, independently-generated data), or that network performance is not the binding constraint on efficiency in this particular factory configuration. We recommend this analysis be repeated on real production telemetry before drawing operational conclusions.

## 1. Introduction

In Industry 4.0 and emerging Industry 5.0 environments, machines increasingly depend on low-latency, high-reliability communication for real-time coordination and AI-driven decision-making. The premise motivating this study is that network degradation — rising latency or packet loss — could silently erode manufacturing efficiency without any accompanying mechanical failure, making such degradation easy to misdiagnose as a machine fault rather than a connectivity issue.

This creates a practical problem for manufacturers: without clear evidence of how much network performance actually affects efficiency, investment decisions between network infrastructure and mechanical maintenance are difficult to prioritize correctly. This study directly tests that premise using the provided dataset, asking three concrete questions:

1. Are efficiency drops associated with network latency or packet loss, independent of mechanical conditions?
2. Is there a latency or packet-loss threshold beyond which efficiency reliably degrades?
3. Are certain operation modes more sensitive to network instability than others?

## 2. Dataset Description

The dataset contains 100,000 per-minute telemetry readings from 50 industrial machines, with no missing values and no duplicate rows. Fields fall into four categories:

- **Mechanical:** Temperature_C, Vibration_Hz, Power_Consumption_kW
- **Network:** Network_Latency_ms, Packet_Loss_%
- **Output/Quality:** Production_Speed_units_per_hr, Quality_Control_Defect_Rate_%, Error_Rate_%
- **Categorical/Target:** Operation_Mode (Idle/Active/Maintenance), Efficiency_Status (Low/Medium/High — the target variable)

A key structural feature of this dataset is severe class imbalance in the target variable: Low efficiency accounts for 77.8% of rows, Medium 19.2%, and High only 3.0%. This imbalance is addressed explicitly throughout the analysis, since plain accuracy is a misleading metric under this distribution.

## 3. Methodology

Five complementary, independent methods were used to test the network-efficiency relationship from different angles, so that a negative result in one would not simply be a blind spot of that particular technique:

1. **Descriptive/quality profiling** — missing values, duplicates, IQR-based outlier detection, and distribution shape for all numeric fields.
2. **Correlation analysis** — Pearson correlation coefficients across all numeric variable pairs, to detect linear relationships.
3. **Chi-square tests of independence** — network variables were binned into Low/Medium/High tertiles (using quantile-based cuts) and cross-tabulated against Efficiency_Status, both across the full dataset and separately within each Operation_Mode, to detect non-linear/categorical associations that correlation could miss.
4. **Predictive modeling** — a Random Forest classifier (with class-balanced weighting, given the target imbalance) was trained on genuine input variables to quantify, via feature importances and per-class recall, how much predictive signal network variables carry relative to mechanical variables.
5. **Custom KPIs** — four metrics specified in the project brief (Network Stability Index, Latency Sensitivity Score, Packet Loss Impact Ratio, Network-Efficiency Threshold) were computed to summarize network conditions and their apparent relationship to output quality.

## 4. Findings

### 4.1 Data Quality and Distribution

The dataset contains no missing values and no duplicate rows. All numeric fields fall within physically plausible ranges (e.g., temperature between 30–80°C, percentage fields bounded within 0–100%), and IQR-based outlier detection found **zero outliers across every numeric column**. This is notable: real-world sensor data typically contains at least some natural extremes (sensor glitches, maintenance events, transient spikes). The complete absence of outliers is an early indicator that this dataset may be synthetically generated with tightly bounded or independently sampled distributions, rather than drawn from real factory sensor logs.

### 4.2 Correlation Analysis

A Pearson correlation matrix across all nine numeric variables showed **no meaningful linear relationships** anywhere in the dataset — nearly all pairwise correlations fell within ±0.02 of zero, including between the network variables (latency, packet loss) and every output/quality variable (production speed, defect rate, error rate). Mechanical variables (temperature, vibration, power) showed the same near-zero pattern against outcomes. No variable pair in the dataset showed a linear relationship strong enough to be practically meaningful.

### 4.3 Network Quality Bands and Chi-Square Tests

Network_Latency_ms and Packet_Loss_% were each split into Low/Medium/High tertile bands (via quantile-based binning, ensuring roughly equal group sizes) and cross-tabulated against Efficiency_Status. Chi-square tests of independence found no statistically significant association for either variable:

| Variable | χ² statistic | df | p-value |
|---|---|---|---|
| Latency Band | 5.69 | 4 | 0.224 |
| Packet Loss Band | 4.32 | 4 | 0.37 |

Both p-values are well above the conventional 0.05 significance threshold, indicating the observed distribution of efficiency across network bands is consistent with random variation, not a genuine association.

### 4.4 Operation Mode Interaction

To rule out the possibility that a network effect exists but is masked when averaged across all operation modes, the latency and packet-loss chi-square tests were repeated separately within each Operation_Mode (Idle, Active, Maintenance). No mode showed a significant association — p-values across all modes and both network variables ranged from approximately 0.37 to 0.7, all well above the 0.05 threshold. This rules out a mode-specific effect being obscured in the aggregate analysis.

### 4.5 Predictive Modeling

An initial Random Forest classifier trained on all available numeric features (excluding only the target and identifiers) achieved perfect or near-perfect precision, recall, and F1-scores across all three efficiency classes. This result was treated as a red flag rather than a success, since near-perfect classification on real-world-style data is a strong indicator of **data leakage** — a situation where an input feature effectively encodes the target rather than genuinely predicting it. Inspection of feature importances confirmed this: Error_Rate_% (60.1%) and Production_Speed_units_per_hr (39.3%) together accounted for 99.4% of the model's decision-making, strongly suggesting these output/quality variables were used to directly construct the Efficiency_Status label during data generation.

The model was rebuilt using only genuine, independent input variables — Temperature_C, Vibration_Hz, Power_Consumption_kW, Network_Latency_ms, Packet_Loss_%, and Predictive_Maintenance_Score — excluding all output/quality-derived fields. Performance dropped sharply:

| Class | Precision | Recall | F1-score | Support |
|---|---|---|---|---|
| High | 0.00 | 0.00 | 0.00 | 597 |
| Low | 0.78 | 0.94 | 0.85 | 15,565 |
| Medium | 0.20 | 0.06 | 0.09 | 3,838 |
| **Accuracy** | | | **0.74** | 20,000 |

The model failed to identify any High-efficiency cases (0.00 recall) and captured only 6% of Medium-efficiency cases, with strong performance limited to the majority Low class. The 74% overall accuracy is misleading in isolation, given it is achievable largely by defaulting toward the majority class. Feature importances in this corrected model were nearly uniform across all six inputs (approximately 16–17% each), including the two network variables — indicating the model found no single variable, network-related or otherwise, that meaningfully distinguishes efficiency classes.

### 4.6 KPI Analysis

The four brief-specified KPIs were computed and support the same conclusion:

- **Network Stability Index** averaged ~50 with a roughly even spread (25th–75th percentile: 35–64), consistent with latency and packet loss being independently and evenly distributed rather than clustered around specific problem conditions.
- **Packet Loss Impact Ratio** showed a −0.64% change in defect rate and −0.28% change in error rate between low- and high-packet-loss periods — negligible in magnitude and in the opposite direction from the brief's hypothesis (worse packet loss did not correspond to worse quality).
- **Latency Sensitivity Score**, calculated as the slope of production speed against latency within each latency band, was near-zero and inconsistent in sign across bands (Low: +0.03, Medium: −0.41, High: −0.17 units/hr per ms) — not a practically meaningful effect.
- **Network-Efficiency Threshold** — intended to identify the latency value at which Low-efficiency probability crosses 50% — returned a value in the very first (lowest-latency) bin tested. This is not a meaningful threshold; it is an artifact of Low efficiency already representing 78% of the entire dataset regardless of latency, meaning virtually any bin crosses 50% immediately.

## 5. Discussion

Across five independent analytical approaches — spanning linear, categorical, model-based, and summary-metric methods — this study found no evidence that network performance (latency or packet loss) meaningfully affects manufacturing efficiency, quality, or production speed in this dataset. This consistency across methods strengthens confidence in the negative result: it is not an artifact of any single technique's blind spot.

The most likely explanation is that the dataset was synthetically generated with each variable sampled independently, rather than simulating a genuine underlying causal process linking network conditions to efficiency outcomes. This is supported by several converging signals: the complete absence of outliers, the uniformly near-zero correlations across *all* variable pairs (not just network ones), and the nearly equal feature importances in the corrected classifier — patterns that would be unusual in real sensor telemetry, where at least some variables typically show natural relationships or extremes.

This does not mean the underlying premise of the brief is wrong in the real world — only that this particular dataset does not provide evidence for or against it. A genuine test of the network-efficiency relationship would require either real production telemetry or a synthetic dataset explicitly constructed to encode the hypothesized relationship.

## 6. Limitations

- **Suspected synthetic data:** as discussed above, several structural indicators suggest this dataset may not reflect real causal dynamics between network conditions and efficiency.
- **Cross-sectional snapshot:** the dataset covers a fixed time window per machine without long-term trend data, limiting the ability to study lagged or cumulative network effects (e.g., sustained latency over hours rather than instantaneous readings).
- **No ground-truth validation:** Efficiency_Status is a provided label without an independently verifiable definition, so its relationship to the underlying mechanical/network readings cannot be fully audited.
- **Correlational, not causal:** even where associations exist, none of the methods used here establish causation; a chi-square or classifier result reflects statistical association only.

## 7. Recommendations

1. **Validate against real telemetry before acting operationally.** Given the strong indicators of synthetic/independent data generation, we recommend against making network infrastructure investment decisions based solely on this dataset. The analysis pipeline built here (EDA, banding, chi-square testing, leak-checked classification, KPI computation) is reusable and should be re-run on real production data when available.
2. **If real data confirms this pattern**, network infrastructure investment may be de-prioritized relative to other efficiency levers (e.g., predictive maintenance, mechanical calibration), since this analysis found mechanical variables similarly uninformative — suggesting efficiency in this dataset may be driven by factors not captured in the current feature set at all.
3. **Always test for data leakage before trusting a high-performing model.** The initial classifier's apparent 100% accuracy would have led to a false conclusion (that network and mechanical variables strongly predict efficiency) had feature importances not been inspected. This is a general best practice worth institutionalizing in any future modeling work at Thales.
4. **Expand the feature set if repeating this study**, to include variables not present here — e.g., time-of-day, machine age/maintenance history, or network topology details — which may carry signal the current dataset lacks.

## 8. Conclusion

This study set out to quantify the impact of 6G network performance on manufacturing efficiency in a smart factory setting. Using five independent, complementary methods, we consistently found no statistically or practically significant relationship between network conditions and efficiency outcomes in the provided dataset. Rather than force a positive finding, we report this negative result transparently, along with strong structural evidence that the dataset itself may not encode a genuine causal relationship — and recommend this analysis be repeated on real operational data before informing infrastructure decisions.
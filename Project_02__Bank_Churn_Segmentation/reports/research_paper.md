# Customer Segmentation & Churn Pattern Analytics in European Banking

**Prepared for:** The European Central Bank (via Unified Mentor)
**Dataset:** European_Bank.csv — 10,000 customers, 3 countries, 14 fields

---

## Abstract

This study analyzes customer churn among 10,000 European bank customers to identify which customer segments carry the highest churn risk, using segmentation across geography, age, gender, credit score, tenure, and account balance. Using chi-square significance testing, interaction analysis, revenue-at-risk quantification, and a Random Forest classifier, we find that churn is strongly and unevenly concentrated: customers in Germany, in the 46-60 age band, and female customers each show substantially elevated churn independently of one another, with the highest-risk compound segment — German women aged 46-60 — reaching a churn rate of over 60%. Churned customers also hold disproportionately more balance than retained customers, meaning churn's financial impact outpaces its headcount impact. Member engagement emerged as the most operationally actionable factor, with inactive members churning at nearly double the rate of active ones. We recommend the bank shift from uniform retention spending toward targeted intervention on these identified high-risk segments.

## 1. Introduction

Customer churn is one of the largest hidden costs in retail banking: every departing customer represents lost lifetime value and a costlier replacement through new acquisition. Banks typically track an aggregate churn rate, but this single number obscures which customers are actually at risk and why — making retention strategy generic and reactive rather than targeted.

This study addresses that gap directly, using customer-level data to answer three core questions specified in the project brief:

1. Which customer groups are most likely to churn?
2. How does churn differ across countries, age groups, and financial profile?
3. Is churn concentrated among high-value or low-value customers?

## 2. Dataset Description

The dataset contains 10,000 customer records with no missing values and no duplicates. CustomerId is confirmed unique per row (10,000 unique values matching 10,000 rows) and used only as an identifier, never as an analytical feature; Surname was excluded entirely, as specified in the brief. Fields include demographic information (Geography, Gender, Age), financial profile (CreditScore, Balance, EstimatedSalary), engagement indicators (Tenure, NumOfProducts, HasCrCard, IsActiveMember), and the target variable, Exited (1 = churned, 0 = retained). The overall churn rate is 20.37%.

Five segmentation dimensions were constructed per the brief: Age Bands (<30, 30-45, 46-60, 60+, using the brief's specified cutoffs), Credit Score Bands (Low <580, Medium 580-700, High >700, using standard credit scoring convention), Tenure Groups (New 0-2 years, Mid-term 3-6 years, Long-term 7+ years), and Balance Segments (Zero, Low <€100,000, High ≥€100,000). All resulting segments contained substantial sample sizes (smallest: Age 60+ at n=464), supporting reliable conclusions across every segment.

## 3. Methodology

1. **Data validation** — missing values, duplicates, and identifier field verification.
2. **Sample-size verification** — before treating any extreme percentage as a finding, underlying group sizes were checked (e.g., customers with 4 bank products showed 100% churn, but represent only 60 of 10,000 customers — reported with an explicit low-confidence caveat rather than as a headline result).
3. **Segment-wise churn analysis** — churn rate computed within each of the five segmentation dimensions, tested for statistical significance via chi-square tests of independence.
4. **Interaction analysis** — Geography × Age and Gender × Age/Geography cross-tabulations, to determine whether risk factors compound independently or overlap.
5. **High-value customer analysis** — churn rate and revenue-at-risk quantification among top-balance customers, comparing balance-based versus salary-based patterns.
6. **Custom KPIs** — five metrics per the brief: Overall Churn Rate, Segment Churn Rate, High-Value Churn Ratio, Geographic Risk Index, and Engagement Drop Indicator.
7. **Predictive modeling** — a Random Forest classifier using genuine customer profile variables (excluding identifiers), evaluated via per-class precision/recall given the class imbalance, with feature importance ranking to cross-validate the statistical findings.

## 4. Findings

### 4.1 Segment-Wise Churn Rates and Significance

| Segment | Churn Rate Range | Chi-square | p-value | Significant? |
|---|---|---|---|---|
| Geography | 16.15% (France) – 32.44% (Germany) | 301.26 | <0.00001 | Yes |
| Gender | 16.46% (Male) – 25.07% (Female) | 112.92 | <0.00001 | Yes |
| Age Band | 7.50% (<30) – 51.12% (46-60) | 1241.61 | <0.00001 | Yes (strongest effect) |
| Balance Segment | 13.82% (Zero) – 25.23% (High) | 165.61 | <0.00001 | Yes |
| Credit Score Band | 19.77% – 22.15% | 6.14 | 0.046 | Marginal, weak effect |
| Tenure Group | 19.51% – 21.15% | 2.75 | 0.253 | Not significant |

Age is the dominant driver of churn, rising sharply from 7.5% under age 30 to a peak of 51.1% in the 46-60 band, before declining to 24.8% for customers over 60 — a non-monotonic pattern, not a simple linear age effect. Geography, Gender, and Balance Segment all show strong, highly significant associations. Tenure — how long a customer has held their account — shows no meaningful relationship to churn, and Credit Score shows only a marginal effect too small to be practically actionable on its own.

### 4.2 Interaction Effects

Geography and Age act as independent, compounding risk factors rather than one explaining the other: Germany shows elevated churn across every age band, not concentrated in a single group. The Germany × 46-60 combination reaches 67.33% churn — the highest cell identified in the analysis. Gender shows a consistent gap (Female > Male) across every country and every age band, with the gap most pronounced in Germany (~10 percentage points, versus ~8 points in France and Spain). The compound profile of a German woman aged 46-60 represents the highest concentration of churn risk found in this study, with that specific subgroup's churn rate exceeding 60%.

### 4.3 High-Value Customer and Revenue Risk Analysis

Churned customers hold €91,109 in average balance, approximately 25% more than retained customers (€72,745). As a result, churned customers account for 24.26% of total customer balance, despite representing only 20.37% of customers — churn's financial impact exceeds its headcount impact. Customers in the top 25% by balance (≥€127,644) show a churn rate of 23.68%, modestly elevated above the 20.37% baseline (a ratio of 1.16x) — a real but not dramatic individual-level effect. Estimated salary, unlike balance held at the bank, showed no comparable distinguishing pattern between churned and retained customers, indicating that balance specifically held with this institution — not general customer wealth — is the more relevant churn signal.

### 4.4 Custom KPIs

- **Overall Churn Rate:** 20.37%
- **Geographic Risk Index:** Germany 159.3 (59% above average), France 79.3, Spain 81.9 — both below average
- **High-Value Churn Ratio:** 1.16 — high-value customers churn 16% more often than the overall average
- **Engagement Drop Indicator:** Inactive members churn at 26.85% versus 14.27% for active members — a 12.58 percentage-point gap, the largest directly actionable signal identified in this analysis, since member engagement (unlike age or geography) can be influenced through direct intervention.

### 4.5 Predictive Modeling

A Random Forest classifier, trained on genuine profile variables (Credit Score, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, and one-hot encoded Geography/Gender), achieved 85% accuracy against a 79.6% majority-class baseline, with 61% recall and 63% precision on the churned class — a legitimate, usable predictive result, not an artifact of leakage or class imbalance.

Feature importances placed Age at the top (0.248), consistent with its dominant chi-square effect. Balance, EstimatedSalary, NumOfProducts, and CreditScore followed closely. Notably, Geography_Germany ranked comparatively low (0.032) in the model despite showing the strongest standalone chi-square association among categorical variables. This likely reflects that Age, Balance, and CreditScore collectively capture overlapping risk signal that Geography also captures — feature importance measures each variable's unique marginal contribution once other correlated variables are already accounted for, while chi-square measures raw standalone association; the two methods can reasonably diverge for correlated variables without contradicting one another.

## 5. Discussion

Churn in this dataset is not random or evenly distributed — it concentrates sharply around identifiable, stable customer characteristics. Age is the single strongest driver, with a distinctive peak in the 46-60 range rather than a simple "older customers leave more" pattern, suggesting this age band may face a particular life-stage or financial transition (e.g., retirement planning, competing financial products) that increases their propensity to switch banks. Germany's elevated churn, holding consistently across every age and gender combination, points to a market-specific factor — potentially competitive intensity, product fit, or service quality specific to the German market — that merits further qualitative investigation beyond what this dataset can explain alone.

The finding that higher-balance customers churn somewhat more, not less, than lower-balance customers runs counter to a common assumption that wealthier customers are inherently more "sticky." A plausible explanation is that high-balance customers are more actively courted by competitor banks and have more to gain from shopping around, whereas low-balance or zero-balance customers may simply be less engaged with banking generally, regardless of loyalty.

## 6. Limitations

- **Cross-sectional data:** the dataset captures each customer's status at one point in time; it cannot show the trajectory of engagement or balance leading up to churn, only a snapshot.
- **No stated reason for churn:** the data indicates *that* a customer left, but not *why* — geographic and demographic patterns are strong correlates, not confirmed causes, and could reflect unmeasured factors specific to each market or life stage.
- **Small-sample segments require caution:** the NumOfProducts=4 group (n=60, 100% churn) and, to a lesser extent, NumOfProducts=3 (n=266, ~83% churn) are based on comparatively small samples and should not be treated with the same confidence as the larger, thousands-strong segments.
- **Correlational, not causal:** all associations reported, however strong, reflect statistical relationships rather than proven causal mechanisms.

## 7. Recommendations

1. **Prioritize retention outreach toward the compound high-risk profile**: customers in Germany, aged 46-60, particularly women, represent the highest concentration of churn risk identified. Targeted retention offers or proactive relationship management for this specific segment would likely yield the highest return on retention investment.
2. **Investigate Germany specifically**: since Germany's elevated churn holds across all demographics, this points to a market-level issue (competition, pricing, product fit, service quality) rather than a demographic one. A qualitative follow-up — customer surveys or exit interviews in the German market — would help identify the specific driver.
3. **Launch engagement-focused retention campaigns**: the 12.6 percentage-point gap between active and inactive members is the most directly actionable finding in this study. Automated engagement campaigns (app reminders, personalized offers, proactive check-ins) targeting members showing early signs of disengagement could meaningfully reduce churn before it happens.
4. **Treat high-balance customer retention as a revenue-protection priority**: while high-value customers do not churn dramatically more often individually, their departures cost the bank disproportionately in absolute terms. Dedicated relationship managers or premium retention offers for top-quartile-balance customers are likely to be cost-justified given the revenue at stake.
5. **Do not prioritize tenure- or credit-score-based retention programs**: neither showed a meaningful, actionable relationship to churn in this analysis, and retention resources aimed at these dimensions would likely be poorly targeted.

## 8. Conclusion

This study identified clear, statistically robust, and actionable churn patterns among European bank customers. Age, geography, gender, and account balance each independently and significantly predict elevated churn risk, compounding into a specific highest-risk profile: German women aged 46-60. Member engagement stands out as the most directly actionable lever available to the bank. These findings support a shift from generic, blanket retention spending toward targeted, segment-specific intervention, with the greatest expected impact concentrated in a well-defined, identifiable share of the customer base.
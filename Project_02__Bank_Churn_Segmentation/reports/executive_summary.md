# Executive Summary: Customer Churn Segmentation Analysis

**Prepared for:** European Central Bank stakeholders

## The Question

One in five bank customers leaves — but which ones, and why? Without knowing where churn concentrates, retention spending is spread thin and generically, instead of targeted where it will have the most impact.

## What We Did

We analyzed 10,000 customer records, segmenting churn by geography, age, gender, credit profile, tenure, and account balance, and built a predictive model to confirm the findings independently.

## What We Found

**Churn is heavily concentrated, not evenly spread.** Three factors matter most, and they compound:

- **Geography**: German customers churn at 32%, roughly double France and Spain (16-17% each).
- **Age**: churn peaks sharply at 51% for customers aged 46-60, more than six times the rate for customers under 30.
- **Gender**: female customers churn at 25%, versus 17% for male customers, consistently across every country and age group.

The **highest-risk customer profile is a German woman aged 46-60** — this specific group's churn rate exceeds 60%.

**Money matters too.** Customers who leave hold, on average, 25% more balance than those who stay — meaning churn costs the bank more in real money than the customer-count percentage alone suggests: nearly a quarter of total customer balance is lost to churn.

**The most fixable factor: engagement.** Customers who are inactive churn at nearly double the rate of active ones (27% vs 14%). Unlike age or nationality, this is something the bank can directly influence.

## What Doesn't Matter

How long a customer has held their account (tenure) shows no meaningful link to churn — retention programs built around tenure would be misdirected. Credit score shows only a very weak effect.

## Recommendations

1. **Target retention efforts at the highest-risk profile**: German customers aged 46-60, especially women.
2. **Investigate the German market specifically** — since elevated churn holds across every age and gender group there, this points to a market-wide issue (competition, pricing, service) rather than a demographic one.
3. **Launch engagement campaigns** for customers showing early signs of inactivity — this is the single most actionable lever identified.
4. **Protect high-balance relationships** — their departures cost disproportionately more than their numbers suggest, justifying dedicated retention attention.
5. **Do not prioritize tenure-based retention programs** — the data does not support them.

## Full Technical Detail

See the accompanying research paper for complete methodology and statistical results, and the interactive dashboard for direct segment-level exploration.
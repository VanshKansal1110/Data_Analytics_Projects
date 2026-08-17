import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from kpi import overall_churn_rate, segment_churn_rate, high_value_churn_ratio, geographic_risk_index, engagement_drop_indicator

st.set_page_config(page_title="Bank Customer Churn Analytics", layout="wide", page_icon="🏦")

# ---- Custom styling for a more polished look ----
st.markdown("""
<style>
[data-testid="stMetricValue"] { font-size: 28px; }
.stTabs [data-baseweb="tab"] { font-size: 16px; padding: 10px 20px; }
</style>
""", unsafe_allow_html=True)

st.title("🏦 Customer Segmentation & Churn Pattern Analytics")
st.caption("European Banking — Interactive Churn Risk Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'raw', 'European_Bank.csv'))
    df['Age_Band'] = pd.cut(df['Age'], bins=[18, 30, 45, 60, 100],
                             labels=['<30', '30-45', '46-60', '60+'], right=True)
    df['CreditScore_Band'] = pd.cut(df['CreditScore'], bins=[0, 580, 700, 900],
                                      labels=['Low', 'Medium', 'High'])
    df['Tenure_Group'] = pd.cut(df['Tenure'], bins=[-1, 2, 6, 20],
                                  labels=['New', 'Mid-term', 'Long-term'])
    df['Balance_Segment'] = pd.cut(df['Balance'], bins=[-1, 0, 100000, df['Balance'].max()],
                                     labels=['Zero-balance', 'Low-balance', 'High-balance'])
    return df

df = load_data()

st.sidebar.header("🔍 Filters")

selected_geo = st.sidebar.multiselect("Geography", df['Geography'].unique(), default=df['Geography'].unique())
selected_gender = st.sidebar.multiselect("Gender", df['Gender'].unique(), default=df['Gender'].unique())
selected_age = st.sidebar.multiselect("Age Band", df['Age_Band'].unique(), default=df['Age_Band'].unique())
selected_balance = st.sidebar.multiselect("Balance Segment", df['Balance_Segment'].unique(), default=df['Balance_Segment'].unique())
selected_active = st.sidebar.multiselect("Active Member", ['Active', 'Inactive'], default=['Active', 'Inactive'])

active_map = {'Active': 1, 'Inactive': 0}
active_vals = [active_map[a] for a in selected_active]

filtered_df = df[
    (df['Geography'].isin(selected_geo)) &
    (df['Gender'].isin(selected_gender)) &
    (df['Age_Band'].isin(selected_age)) &
    (df['Balance_Segment'].isin(selected_balance)) &
    (df['IsActiveMember'].isin(active_vals))
]

st.sidebar.markdown("---")
st.sidebar.metric("Filtered Customers", f"{len(filtered_df):,}")
st.sidebar.metric("Filtered Churn Rate", f"{filtered_df['Exited'].mean()*100:.2f}%" if len(filtered_df) > 0 else "N/A")

st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Overall Churn Rate", f"{filtered_df['Exited'].mean()*100:.1f}%" if len(filtered_df) else "N/A")
col2.metric("Customers Shown", f"{len(filtered_df):,}")
col3.metric("Avg Balance", f"€{filtered_df['Balance'].mean():,.0f}" if len(filtered_df) else "N/A")
col4.metric("High-Value Churn Ratio", f"{high_value_churn_ratio(filtered_df)['ratio']:.2f}x" if len(filtered_df) > 20 else "N/A")
inactive_gap = engagement_drop_indicator(filtered_df)['gap_percentage_points'] if len(filtered_df) > 20 else None
col5.metric("Engagement Gap", f"{inactive_gap:.1f} pts" if inactive_gap else "N/A")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Overall & Geography", "👥 Age & Tenure", "💰 High-Value Explorer", "🔎 Drill-Down"
])

# ================= TAB 1 =================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Churn Rate by Geography")
        fig, ax = plt.subplots(figsize=(6, 4.5))
        geo_churn = filtered_df.groupby('Geography')['Exited'].mean() * 100
        colors = ['#d62728' if v == geo_churn.max() else '#4C72B0' for v in geo_churn]
        geo_churn.plot(kind='bar', ax=ax, color=colors)
        ax.set_ylabel("Churn %")
        for i, v in enumerate(geo_churn):
            ax.text(i, v + 0.5, f"{v:.1f}%", ha='center', fontweight='bold')
        st.pyplot(fig)

    with col2:
        st.subheader("Overall Churn Split")
        fig2, ax2 = plt.subplots(figsize=(6, 4.5))
        churn_counts = filtered_df['Exited'].value_counts()
        ax2.pie(churn_counts, labels=['Retained', 'Churned'], autopct='%1.1f%%',
                colors=['#4C72B0', '#d62728'], startangle=90, explode=[0, 0.08])
        st.pyplot(fig2)

    st.subheader("Geography × Age Band Heatmap")
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    pivot = filtered_df.pivot_table(values='Exited', index='Geography', columns='Age_Band', aggfunc='mean') * 100
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='Reds', ax=ax3, cbar_kws={'label': 'Churn %'})
    st.pyplot(fig3)

# ================= TAB 2 =================
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Churn Rate by Age Band")
        fig4, ax4 = plt.subplots(figsize=(6, 4.5))
        age_churn = filtered_df.groupby('Age_Band')['Exited'].mean() * 100
        age_churn.plot(kind='bar', ax=ax4, color='#dd8452')
        ax4.set_ylabel("Churn %")
        st.pyplot(fig4)

    with col2:
        st.subheader("Churn Rate by Tenure Group")
        fig5, ax5 = plt.subplots(figsize=(6, 4.5))
        tenure_churn = filtered_df.groupby('Tenure_Group')['Exited'].mean() * 100
        tenure_churn.plot(kind='bar', ax=ax5, color='#55a868')
        ax5.set_ylabel("Churn %")
        st.pyplot(fig5)

    st.subheader("Gender × Age Band")
    fig6, ax6 = plt.subplots(figsize=(10, 4.5))
    gender_age = filtered_df.pivot_table(values='Exited', index='Age_Band', columns='Gender', aggfunc='mean') * 100
    gender_age.plot(kind='bar', ax=ax6)
    ax6.set_ylabel("Churn %")
    st.pyplot(fig6)

# ================= TAB 3 =================
with tab3:
    st.subheader("Balance vs Churn")
    col1, col2 = st.columns(2)

    with col1:
        fig7, ax7 = plt.subplots(figsize=(6, 4.5))
        sns.boxplot(data=filtered_df, x='Exited', y='Balance', ax=ax7)
        ax7.set_xticklabels(['Retained', 'Churned'])
        st.pyplot(fig7)

    with col2:
        fig8, ax8 = plt.subplots(figsize=(6, 4.5))
        seg_churn = filtered_df.groupby('Balance_Segment')['Exited'].mean() * 100
        seg_churn.plot(kind='bar', ax=ax8, color='#8172B2')
        ax8.set_ylabel("Churn %")
        st.pyplot(fig8)

    st.subheader("Revenue at Risk")
    total_bal = filtered_df['Balance'].sum()
    churned_bal = filtered_df[filtered_df['Exited'] == 1]['Balance'].sum()
    pct = (churned_bal / total_bal * 100) if total_bal > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Balance", f"€{total_bal:,.0f}")
    c2.metric("Balance Lost to Churn", f"€{churned_bal:,.0f}")
    c3.metric("% of Balance at Risk", f"{pct:.1f}%")

# ================= TAB 4 =================
with tab4:
    st.subheader("Drill-Down: Explore Any Segment Combination")
    drill_col = st.selectbox("Choose a dimension to break down churn by:",
                              ['Geography', 'Gender', 'Age_Band', 'CreditScore_Band', 'Tenure_Group', 'Balance_Segment'])

    fig9, ax9 = plt.subplots(figsize=(10, 5))
    drill_churn = filtered_df.groupby(drill_col)['Exited'].mean() * 100
    drill_churn.sort_values(ascending=False).plot(kind='barh', ax=ax9, color='#c44e52')
    ax9.set_xlabel("Churn %")
    st.pyplot(fig9)

    st.subheader("Raw Filtered Data")
    st.dataframe(filtered_df[['CustomerId', 'Geography', 'Gender', 'Age', 'Balance',
                               'NumOfProducts', 'IsActiveMember', 'Exited']], use_container_width=True)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '', 'src'))

from kpi import network_stability_index, packet_loss_impact_ratio

st.set_page_config(page_title="6G Network vs Manufacturing Efficiency", layout="wide")

st.title("6G Network Performance vs Manufacturing Efficiency")
st.caption("Thales Group — Smart Factory Analytics")

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '', 'data', 'raw', 'Thales_Group_Manufacturing.csv'))    
    df['Latency_Band'] = pd.qcut(df['Network_Latency_ms'], 3, labels=['Low', 'Medium', 'High'])
    df['PacketLoss_Band'] = pd.qcut(df['Packet_Loss_%'], 3, labels=['Low', 'Medium', 'High'])
    df['Network_Stability_Index'] = network_stability_index(df)
    return df

df = load_data()

st.sidebar.header("Filters")

selected_mode = st.sidebar.multiselect(
    "Operation Mode",
    options=df['Operation_Mode'].unique(),
    default=df['Operation_Mode'].unique()
)

selected_latency_band = st.sidebar.multiselect(
    "Latency Band",
    options=df['Latency_Band'].unique(),
    default=df['Latency_Band'].unique()
)

selected_efficiency = st.sidebar.multiselect(
    "Efficiency Status",
    options=df['Efficiency_Status'].unique(),
    default=df['Efficiency_Status'].unique()
)

filtered_df = df[
    (df['Operation_Mode'].isin(selected_mode)) &
    (df['Latency_Band'].isin(selected_latency_band)) &
    (df['Efficiency_Status'].isin(selected_efficiency))
]

st.write(f"Showing {len(filtered_df):,} of {len(df):,} rows")
st.dataframe(filtered_df.head())

tab1, tab2, tab3 = st.tabs([
    "Network Performance Overview",
    "Network vs Efficiency",
    "Quality & Error Impact",
])

with tab1:
    st.subheader("Network Performance Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Latency (ms)", f"{filtered_df['Network_Latency_ms'].mean():.2f}")
    col2.metric("Avg Packet Loss (%)", f"{filtered_df['Packet_Loss_%'].mean():.2f}")
    col3.metric("Avg Network Stability Index", f"{filtered_df['Network_Stability_Index'].mean():.2f}")

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.histplot(filtered_df['Network_Latency_ms'], bins=30, ax=ax1)
    ax1.set_title("Latency Distribution")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.histplot(filtered_df['Packet_Loss_%'], bins=30, ax=ax2)
    ax2.set_title("Packet Loss Distribution")
    st.pyplot(fig2)

with tab2:
    st.subheader("Efficiency Distribution by Network Quality")

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    crosstab_pct = pd.crosstab(filtered_df['Latency_Band'], filtered_df['Efficiency_Status'], normalize='index') * 100
    crosstab_pct.plot(kind='bar', stacked=True, ax=ax3)
    ax3.set_title("Efficiency % by Latency Band")
    ax3.set_ylabel("Percentage")
    st.pyplot(fig3)

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=filtered_df, x='Efficiency_Status', y='Network_Latency_ms', ax=ax4)
    ax4.set_title("Latency Spread by Efficiency Status")
    st.pyplot(fig4)

with tab3:
    st.subheader("Quality & Error Impact")

    fig5, ax5 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=filtered_df.sample(min(2000, len(filtered_df))), 
                     x='Packet_Loss_%', y='Error_Rate_%', alpha=0.4, ax=ax5)
    ax5.set_title("Error Rate vs Packet Loss (sampled)")
    st.pyplot(fig5)

    fig6, ax6 = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=filtered_df, x='PacketLoss_Band', y='Quality_Control_Defect_Rate_%', ax=ax6)
    ax6.set_title("Defect Rate by Packet Loss Band")
    st.pyplot(fig6)
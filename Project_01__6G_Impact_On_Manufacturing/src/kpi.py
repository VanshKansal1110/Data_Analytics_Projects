"""
KPI calculation functions for the 6G Network vs Manufacturing Efficiency project.

Note: EDA and modeling found no statistically significant relationship between
network variables and Efficiency_Status. These KPIs are therefore reported as
descriptive summaries of network conditions, not as proven drivers of efficiency.
"""

import pandas as pd
import numpy as np


def network_stability_index(df):
    """
    Composite 0-100 score per row combining normalized latency + packet loss.
    Lower score = more stable network conditions. 100 = worst observed conditions.
    """
    latency_norm = (df['Network_Latency_ms'] - df['Network_Latency_ms'].min()) / \
                   (df['Network_Latency_ms'].max() - df['Network_Latency_ms'].min())
    packetloss_norm = (df['Packet_Loss_%'] - df['Packet_Loss_%'].min()) / \
                       (df['Packet_Loss_%'].max() - df['Packet_Loss_%'].min())
    return ((latency_norm + packetloss_norm) / 2) * 100


def packet_loss_impact_ratio(df):
    """
    % difference in mean Defect_Rate and Error_Rate between low- and
    high-packet-loss periods (bottom vs top tertile).
    """
    low = df[df['PacketLoss_Band'] == 'Low']
    high = df[df['PacketLoss_Band'] == 'High']

    defect_change = ((high['Quality_Control_Defect_Rate_%'].mean() -
                       low['Quality_Control_Defect_Rate_%'].mean()) /
                      low['Quality_Control_Defect_Rate_%'].mean()) * 100

    error_change = ((high['Error_Rate_%'].mean() -
                      low['Error_Rate_%'].mean()) /
                     low['Error_Rate_%'].mean()) * 100

    return {'defect_rate_change_%': defect_change, 'error_rate_change_%': error_change}

def latency_sensitivity_score(df):
    """
    Slope of Production_Speed_units_per_hr vs Network_Latency_ms within each
    Latency_Band. Tells you: within a given network condition, does speed
    change as latency changes further?
    """
    results = {}
    for band in df['Latency_Band'].unique():
        subset = df[df['Latency_Band'] == band]
        slope = np.polyfit(subset['Network_Latency_ms'],
                            subset['Production_Speed_units_per_hr'], 1)[0]
        results[band] = slope
    return results


def network_efficiency_threshold(df, step=2):
    """
    Finds the latency (ms) value where P(Efficiency_Status == 'Low') crosses 50%,
    by binning latency into small increments and checking proportion Low in each bin.
    Returns None if no bin crosses 50% (i.e. no clear threshold exists).
    """
    bins = np.arange(df['Network_Latency_ms'].min(), df['Network_Latency_ms'].max(), step)
    df_binned = df.copy()
    df_binned['Latency_Bin'] = pd.cut(df_binned['Network_Latency_ms'], bins)

    prop_low = df_binned.groupby('Latency_Bin', observed=True)['Efficiency_Status'] \
                         .apply(lambda x: (x == 'Low').mean())

    crossing = prop_low[prop_low >= 0.5]
    if crossing.empty:
        return None
    return crossing.index[0]
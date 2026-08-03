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
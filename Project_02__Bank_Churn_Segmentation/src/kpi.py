"""
KPI calculation functions for the Customer Segmentation & Churn Pattern Analytics project.
"""

import pandas as pd


def overall_churn_rate(df):
    """
    % of all customers who exited (churned).
    """
    return df['Exited'].mean() * 100


def segment_churn_rate(df, segment_col):
    """
    Churn % broken down by any segmentation column (e.g. Geography, Age_Band).
    Returns a Series: one churn rate per group in that segment.
    """
    return df.groupby(segment_col)['Exited'].mean() * 100


def high_value_churn_ratio(df, percentile=0.75):
    """
    Churn rate among customers in the top balance percentile, compared to
    the overall churn rate. Returns a dict with both numbers and the ratio
    between them (>1 means high-value customers churn more than average).
    """
    threshold = df['Balance'].quantile(percentile)
    high_value = df[df['Balance'] >= threshold]

    high_value_rate = high_value['Exited'].mean() * 100
    overall_rate = df['Exited'].mean() * 100

    return {
        'high_value_churn_rate_%': high_value_rate,
        'overall_churn_rate_%': overall_rate,
        'ratio': high_value_rate / overall_rate
    }


def geographic_risk_index(df):
    """
    Churn rate per country, indexed against the overall churn rate
    (100 = average risk, >100 = above-average risk, <100 = below-average).
    """
    overall_rate = df['Exited'].mean() * 100
    country_rate = df.groupby('Geography')['Exited'].mean() * 100
    return (country_rate / overall_rate * 100).round(1)


def engagement_drop_indicator(df):
    """
    Compares churn rate between inactive and active members, and the
    percentage-point gap between them.
    """
    active_rate = df[df['IsActiveMember'] == 1]['Exited'].mean() * 100
    inactive_rate = df[df['IsActiveMember'] == 0]['Exited'].mean() * 100

    return {
        'active_member_churn_%': active_rate,
        'inactive_member_churn_%': inactive_rate,
        'gap_percentage_points': inactive_rate - active_rate
    }
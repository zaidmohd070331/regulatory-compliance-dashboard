# kri_pipeline.py
# Automated KRI monitoring pipeline
# Extracts compliance data, evaluates against thresholds,
# and flags breaches for escalation — aligned to CCO reporting standards

import pandas as pd
import numpy as np
from datetime import datetime

def load_kri_data(filepath):
    """Load KRI dataset."""
    df = pd.read_csv(filepath)
    df['reporting_date'] = pd.to_datetime(df['reporting_date'])
    return df

def evaluate_kri_status(row):
    """
    Evaluate each KRI against warning and breach thresholds.
    Logic accounts for both direction types:
    - Some KRIs breach when value is TOO HIGH (e.g. error rates, complaint counts)
    - Some KRIs breach when value is TOO LOW (e.g. training completion %, capital ratio)
    """
    val = row['current_value']
    warn = row['threshold_warning']
    breach = row['threshold_breach']

    # Determine direction: if breach threshold < warning threshold,
    # lower is worse (e.g. training completion %)
    if breach < warn:
        if val <= breach:
            return 'Breach'
        elif val <= warn:
            return 'Warning'
        else:
            return 'Within Threshold'
    else:
        if val >= breach:
            return 'Breach'
        elif val >= warn:
            return 'Warning'
        else:
            return 'Within Threshold'

def calculate_breach_severity(row):
    """
    Calculate how far a KRI has breached its threshold.
    Returns a severity score for prioritisation.
    """
    if row['kri_status'] == 'Within Threshold':
        return 0

    val = row['current_value']
    breach = row['threshold_breach']

    if breach != 0:
        deviation = abs(val - breach) / abs(breach) * 100
    else:
        deviation = 0

    return round(deviation, 2)

def assign_rag_status(status):
    """Map KRI status to RAG for Power BI reporting."""
    mapping = {
        'Breach': 'Red',
        'Warning': 'Amber',
        'Within Threshold': 'Green'
    }
    return mapping.get(status, 'Green')

def run_kri_pipeline(filepath):
    """
    Full KRI monitoring pipeline.
    Returns scored and flagged KRI dataframe.
    """
    df = load_kri_data(filepath)
    df['kri_status'] = df.apply(evaluate_kri_status, axis=1)
    df['breach_severity_pct'] = df.apply(calculate_breach_severity, axis=1)
    df['rag_status'] = df['kri_status'].apply(assign_rag_status)
    df['escalation_required'] = df['kri_status'].apply(
        lambda x: 1 if x == 'Breach' else 0
    )
    return df.sort_values('breach_severity_pct', ascending=False)

def print_dashboard_summary(df):
    """Print MI-style summary report."""
    print("\n" + "="*60)
    print("KRI COMPLIANCE MONITORING DASHBOARD — MI SUMMARY")
    print(f"Reporting Date: {df['reporting_date'].iloc[0].strftime('%d %B %Y')}")
    print("="*60)
    print(f"Total KRIs monitored : {len(df)}")
    print(f"Breached             : {(df['kri_status'] == 'Breach').sum()}")
    print(f"Warning              : {(df['kri_status'] == 'Warning').sum()}")
    print(f"Within Threshold     : {(df['kri_status'] == 'Within Threshold').sum()}")
    print(f"Escalation required  : {df['escalation_required'].sum()}")
    print("\nBreached KRIs (Immediate Escalation Required):")
    breached = df[df['kri_status'] == 'Breach'][[
        'kri_id', 'kri_name', 'business_unit',
        'current_value', 'threshold_breach',
        'breach_severity_pct', 'regulatory_domain'
    ]]
    print(breached.to_string(index=False))
    print("="*60)

if __name__ == "__main__":
    df = run_kri_pipeline("../data/kri_data.csv")
    print_dashboard_summary(df)
    df.to_csv("../reports/kri_monitoring_output.csv", index=False)
    print("\nOutput saved to reports/kri_monitoring_output.csv")

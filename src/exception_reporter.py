# exception_reporter.py
# Generates structured exception reports flagging control breaches
# by severity and regulatory domain — for compliance stakeholder review

import pandas as pd
from kri_pipeline import run_kri_pipeline

SEVERITY_ORDER = ['Breach', 'Warning', 'Within Threshold']

def generate_exception_report(df):
    """
    Generate a structured exception report grouped by
    regulatory domain and severity — mirrors CCO escalation reporting.
    """
    exceptions = df[df['kri_status'].isin(['Breach', 'Warning'])].copy()
    exceptions['status_rank'] = exceptions['kri_status'].map(
        {'Breach': 1, 'Warning': 2}
    )
    exceptions = exceptions.sort_values(
        ['status_rank', 'breach_severity_pct'],
        ascending=[True, False]
    )
    return exceptions

def print_exception_report(df):
    """Print exception report by regulatory domain."""
    exceptions = generate_exception_report(df)
    domains = exceptions['regulatory_domain'].unique()

    print("\n" + "="*60)
    print("EXCEPTION REPORT — COMPLIANCE BREACH SUMMARY")
    print("="*60)

    for domain in domains:
        domain_data = exceptions[exceptions['regulatory_domain'] == domain]
        print(f"\n📋 Regulatory Domain: {domain}")
        print("-" * 40)
        for _, row in domain_data.iterrows():
            status_icon = "🔴" if row['kri_status'] == 'Breach' else "🟡"
            print(f"  {status_icon} [{row['kri_id']}] {row['kri_name']}")
            print(f"     Business Unit : {row['business_unit']}")
            print(f"     Current Value : {row['current_value']} {row['unit']}")
            print(f"     Threshold     : {row['threshold_breach']} {row['unit']}")
            print(f"     Status        : {row['kri_status']}")
            print(f"     Trend         : {row['trend']}")
            print()

    print("="*60)
    print(f"Total exceptions: {len(exceptions)}")
    print(f"  Breaches : {(exceptions['kri_status'] == 'Breach').sum()}")
    print(f"  Warnings : {(exceptions['kri_status'] == 'Warning').sum()}")
    print("="*60)

def export_exception_report(df, output_path):
    """Export exception report to CSV for Power BI ingestion."""
    exceptions = generate_exception_report(df)
    exceptions.to_csv(output_path, index=False)
    print(f"Exception report exported to {output_path}")

if __name__ == "__main__":
    df = run_kri_pipeline("../data/kri_data.csv")
    print_exception_report(df)
    export_exception_report(df, "../reports/exception_report.csv")

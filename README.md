# 📊 Regulatory Compliance Monitoring Dashboard

> Automated KRI monitoring pipeline with real-time threshold evaluation, breach detection, and exception reporting — aligned to CCO regulatory compliance frameworks.

---

## 📌 Business Problem

Regulatory compliance teams must continuously monitor Key Risk Indicators (KRIs) across multiple domains — AML, sanctions, conduct risk, prudential, and more. Manual monitoring is slow, inconsistent, and prone to missed breaches. This project automates the full KRI monitoring lifecycle — from data extraction to breach flagging and MI report generation.

---

## 🎯 Objectives

- Extract and transform KRI data via SQL pipelines
- Evaluate each KRI against warning and breach thresholds automatically
- Generate RAG status (Red / Amber / Green) for Power BI dashboard
- Produce structured exception reports by regulatory domain and severity
- Flag deteriorating trends for proactive escalation

---

## 🏗️ Pipeline Architecture

```
KRI Data (SQL / REST API) → Threshold Evaluation
                          → Breach Detection & RAG Classification
                          → Exception Report Generation
                          → Power BI Dashboard Output
```

---

## 🔬 Methodology

### 1. KRI Data
- 15 KRIs across 8 regulatory domains: AML, Sanctions, Conduct Risk, Data Governance, Cybersecurity, Prudential, Model Risk, Third Party Risk
- Fields: kri_id, business_unit, regulatory_domain, current_value, threshold_warning, threshold_breach, trend

### 2. Threshold Evaluation Logic
- Bidirectional threshold logic:
  - KRIs where **higher = worse** (e.g. error rates, complaint counts)
  - KRIs where **lower = worse** (e.g. training completion %, capital ratio)
- Status: **Breach / Warning / Within Threshold**

### 3. Exception Reporting
- Exceptions grouped by regulatory domain and severity
- Breach severity percentage calculated for prioritisation
- Escalation flag for breached KRIs

### 4. RAG Dashboard
- Green = Within Threshold
- Amber = Warning zone
- Red = Breach — immediate escalation required

### 5. SQL Pipelines
- Full KRI status query with inline RAG classification
- Breached KRIs extraction for escalation
- Domain-level heatmap summary
- Trend analysis for deteriorating KRIs
- Business unit compliance scorecard

---

## 📊 Results

| Metric | Value |
|---|---|
| Total KRIs monitored | 15 |
| Breached (Red) | 4 |
| Warning (Amber) | 5 |
| Within Threshold (Green) | 6 |
| Regulatory domains covered | 8 |

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.10 · SQL |
| Pipeline | Pandas · NumPy |
| Data Extraction | SQL (CASE statements, aggregations) · REST APIs |
| Visualisation | Power BI · Matplotlib · Seaborn |
| Reporting | Structured MI Exception Reports |

---

## 📂 Repository Structure

```
├── data/
│   └── kri_data.csv                  # Synthetic KRI monitoring data
├── notebooks/
│   ├── 01_kri_eda.ipynb
│   └── 02_monitoring_pipeline.ipynb
├── src/
│   ├── kri_pipeline.py               # KRI evaluation & RAG classification
│   ├── exception_reporter.py         # Exception report generation
│   └── sql_queries.sql               # SQL extraction pipelines
├── reports/                          # MI reports & dashboard screenshots
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

```bash
git clone https://github.com/zaidmohd070331/regulatory-compliance-dashboard.git
cd regulatory-compliance-dashboard
pip install -r requirements.txt
python src/kri_pipeline.py
python src/exception_reporter.py
```

---

## 💡 Key Takeaways

- Bidirectional threshold logic is critical — not all KRIs breach in the same direction
- Trend analysis adds forward-looking insight beyond point-in-time breach detection
- Structured exception reports by regulatory domain mirror real CCO escalation workflows
- SQL-based extraction ensures auditability and reproducibility of compliance data

---

# GridAnomalyLab  
## Smart Meter Analytics & Anomaly Detection Engine for AMI Systems

---

## Overview

GridAnomalyLab is a modular analytics and monitoring system designed for Smart Meter data in Advanced Metering Infrastructure (AMI) environments.

It provides an end-to-end pipeline for:

- Electrical feature engineering from raw meter data  
- Rule-based and statistical anomaly detection  
- Grid behavior analysis (active & reactive power dynamics)  
- Operational KPI scoring for system health evaluation  
- Interactive Streamlit dashboard for real-time visualization  

The system is built using real-world electrical engineering principles combined with data-driven analytics techniques.

---

## Industry Context

Modern AMI systems generate high-frequency smart meter data that enables utilities to move beyond billing into operational intelligence:

- Grid observability and real-time monitoring  
- Technical & non-technical loss detection  
- Power quality assessment  
- Load behavior analytics  
- Data-driven operational decision support  

GridAnomalyLab simulates a utility-grade analytics pipeline used in modern distribution network monitoring systems.

---

## Approach

The anomaly detection engine is based on electrical system behavior and statistical thresholds:

- Power Factor deviation indicates inefficiency in load utilization  
- Z-score based detection identifies abnormal load spikes  
- Reactive vs Active power imbalance highlights grid instability  

Each data point is scored and classified as normal or anomalous.

### Streamlit Dashboard Integration

A dedicated **Streamlit dashboard (app/dashboard.py)** has been introduced as the primary visualization layer. It provides:

- Real-time KPI monitoring  
- Time-window based analysis  
- Interactive power flow visualizations  
- Anomaly event exploration  
- Grid state-space visualization (P-Q plane)  

---

## Project Structure

```text
GridAnomalyLab/

├── data/
│   └── ami_data.csv
│
├── outputs/
│   └── (generated reports & artifacts)
│
├── src/
│   ├── config.py              # System configuration & thresholds
│   ├── data_loader.py         # Data ingestion layer
│   ├── features.py            # Electrical feature engineering
│   ├── anomaly.py             # Anomaly detection engine
│   ├── visualization.py       # Plot utilities (optional)
│   └── pipeline.py            # Processing pipeline
│
├── app/
│   └── dashboard.py           # Streamlit analytics dashboard
│
├── main.py                    # Batch pipeline execution
├── requirements.txt
├── README.md
└── .gitignore

```

---

## Pipeline Workflow

### 1. Data Loading
The system loads AMI smart meter data from a CSV file or generates synthetic data for testing and development purposes.

This step ensures:
- Consistent schema handling  
- Time-series readiness  
- Missing value control (if applicable)  

---

### 2. Feature Engineering
Raw electrical signals are transformed into meaningful engineering features inside `src/features.py`.

Computed features include:

- Net Active Power (`kw_net = kw+ - kw-`)  
- Net Reactive Power (`kvar_net = kvar+ - kvar-`)  
- Apparent Power (`kva = √(kw_net² + kvar_net²)`)  
- Power Factor (`pf`)  

These features represent the **operational state of the electrical grid**.

---

### 3. Anomaly Detection
The anomaly engine (`src/anomaly.py`) identifies abnormal behavior using rule-based and statistical methods:

- Power Factor threshold violations  
- Z-score based load deviation detection  
- Reactive vs Active power imbalance  

Each record is assigned:
- Anomaly flag (`anomaly`)  
- Anomaly score (`anomaly_score`)  
- Severity level (`severity`)  

---

### 4. KPI & System Health Scoring
A system-level health metric is computed using anomaly density over a time window:

- Total records  
- Total anomalies  
- Anomaly rate  
- System health score  

This is used to classify grid condition as:
- **Healthy**  
- **Degraded**  
- **Critical**

---

### 5. Streamlit Dashboard (Visualization Layer)
The processed data is visualized using an interactive Streamlit dashboard (`app/dashboard.py`).

It provides:

- Time-window based filtering  
- KPI scorecards for system monitoring  
- Active and reactive power time-series plots  
- Power factor stability trends  
- Load stress analysis  
- Grid state-space visualization (P-Q plane)  
- Anomaly event logs with export option  

This layer transforms raw analytics into **operational intelligence for grid monitoring**.

---

## Features

### Input Meter Parameters

The system processes standard smart meter electrical signals:

- `kw+` → Active Power Import  
- `kw-` → Active Power Export  
- `kvar+` → Reactive Power Import  
- `kvar-` → Reactive Power Export  

---

### Derived Features

These engineered features represent the electrical state of the grid:

- `kw_net` → Net Active Power (Import − Export)  
- `kvar_net` → Net Reactive Power (Import − Export)  
- `kva` → Apparent Power (Combined electrical load magnitude)  
- `pf` → Power Factor (System efficiency indicator)  

---

## Installation

Install all dependencies using:

```bash
pip install -r requirements.txt

```
---

## Requirements

```text
pandas>=1.5
numpy>=1.23
plotly>=5.0
streamlit>=1.28

```

---

## How to Run

Run the full pipeline:
python main.py

Run Streamlit dashboard:
streamlit run app/dashboard.py

---

## Outputs

Generated files inside the outputs folder:
- processed.csv → Final dataset with engineered features and anomaly labels
- report.json → Summary statistics of detected anomalies
- power_trend.png → Time series visualization of active/reactive power
- quadrant.png → Power quadrant (P-Q plane) analysis
- power_factor.png → Power factor stability analysis
- load_stress.png → Grid stress visualization using percentile-based scaling

---

## Visualization Insights

### Power Trend
Shows how active and reactive power vary over time, highlighting consumption behavior and export patterns.

### Power Quadrant
Visualizes system operating regions in the P-Q plane, enabling detection of reactive dominance and instability zones.

### Power Factor
Indicates electrical efficiency and quality of load, with low values highlighting inefficiencies.

### Load Stress
Identifies high stress periods in the grid using normalized apparent power distribution.

---

## Future Enhancements

- Real-time streaming integration using MQTT or Kafka
- Production-grade dashboard using Streamlit or Power BI
- REST API deployment using FastAPI
- Integration with weather, tariff, and demand forecasting models
- Machine learning-based anomaly detection for predictive analytics

---

## Author

U. B. Zaheer  
AMI Systems Lead | Data and AI Enthusiast
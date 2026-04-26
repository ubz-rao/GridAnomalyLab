# GridAnomalyLab  
Smart Meter Anomaly Detection in AMI Systems

---

## Overview

GridAnomalyLab is a modular analytics project for detecting anomalies in Smart Meter data used in Advanced Metering Infrastructure (AMI).

It simulates and analyzes electrical consumption patterns to identify abnormal grid behavior such as:

- Energy theft or non-technical losses  
- Meter malfunction or data corruption  
- Abnormal load spikes  
- Poor power factor conditions  
- Reactive power imbalance  

The project is designed using real-world electrical engineering principles combined with statistical anomaly detection techniques.

---

## Industry Context

Modern utility companies deploy AMI systems to collect high-resolution energy usage data from smart meters.

This data is used for:

- Grid monitoring and optimization  
- Loss detection and reduction  
- Demand forecasting  
- Power quality assessment  
- Operational intelligence for utilities  

GridAnomalyLab replicates a simplified version of such utility analytics pipelines.

---

## Approach

The system uses a rule-based anomaly detection engine grounded in electrical concepts:

- Power Factor deviation indicates inefficiency  
- Z-score identifies abnormal load spikes  
- Reactive vs Active power imbalance detects instability  

Each reading is scored to classify system behavior as normal or anomalous.

---

## Project Structure

```text
GridAnomalyLab/

├── data/
│   └── ami_data.csv
│
├── outputs/
│   └── (outputs)
│
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── features.py
│   ├── anomaly.py
│   ├── visualization.py
│   └── pipeline.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

```

---

## Pipeline Workflow

### 1. Data Loading
Loads AMI smart meter data from CSV or generates synthetic data.

### 2. Feature Engineering
Computes electrical features:

- Net Active Power (kw_net)  
- Net Reactive Power (kvar_net)  
- Apparent Power (kva)  
- Power Factor (pf)  

### 3. Anomaly Detection
Detects abnormal behavior using:

- Power Factor thresholding  
- Rolling Z-score for load spikes  
- Reactive power imbalance rule  

### 4. Visualization
Generates insights using plots:

- Power trend over time  
- Power quadrant distribution  
- Power factor stability  
- Load stress analysis  

### 5. Reporting
Exports:

- Processed dataset  
- Anomaly summary report  
- Visualization images  

---

## Features

Input meter parameters:

- kw+ (Active Import)  
- kw- (Active Export)  
- kvar+ (Reactive Import)  
- kvar- (Reactive Export)  

Derived features:

- kw_net  
- kvar_net  
- kva  
- pf  

---

## Installation

Install dependencies:

pip install -r requirements.txt

---

## Requirements

pandas>=1.5
numpy>=1.23
matplotlib>=3.7

---

## How to Run

Run the full pipeline:

python main.py


---

## Outputs

Generated files inside the outputs folder:

- processed.csv → Final dataset with features and anomaly labels  
- report.json → Summary statistics of anomalies  
- power_trend.png → Time series power visualization  
- quadrant.png → Power quadrant analysis  
- power_factor.png → Power factor behavior  
- load_stress.png → Grid stress visualization  

---

## Visualization Insights

### Power Trend
Shows how import and export power varies over time.

### Power Quadrant
Displays distribution of active vs reactive power with anomaly overlay.

### Power Factor
Indicates system efficiency and electrical quality.

### Load Stress
Highlights high load periods using percentile-based thresholds.

---

## Future Enhancements

- Real-time streaming using MQTT or Kafka  
- Dashboard using Streamlit or Power BI  
- API deployment with FastAPI  
- Integration with weather and tariff data  
- Machine learning based anomaly detection  

---

## Author

U. B. Zaheer  
AMI Systems Lead | Data and AI Enthusiast
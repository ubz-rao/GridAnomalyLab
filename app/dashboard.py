import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

# PATH CONFIG
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from src.config import CONFIG
from src.data_loader import load_data
from src.features import create_features
from src.anomaly import detect_anomalies

# PAGE CONFIG
st.set_page_config(
    page_title="GridAnomalyLab | Analytics Engine",
    layout="wide"
)

st.title("GridAnomalyLab | Analytics Engine")
st.caption("Analytics layer for Smart Meter Anomaly Detection in AMI Systems")

# CONTROL PARAMETERS (INPUTS)
st.sidebar.header("Anomaly Parameters")

pf_threshold = st.sidebar.slider(
    "Low Power Factor Threshold",
    0.1, 1.0, float(CONFIG["pf_threshold"])
)

z_threshold = st.sidebar.slider(
    "Load Deviation Threshold (Z-Score)",
    1.0, 6.0, float(CONFIG["z_threshold"])
)

# DATA PIPELINE (CSV_Data / Dummy Data)
@st.cache_data
def load_pipeline():
    df = load_data(CONFIG["use_dummy"], CONFIG["csv_file"])
    df = create_features(df)
    return df

@st.cache_data
def run_anomaly(df, pf_threshold, z_threshold):
    return detect_anomalies(df.copy(), pf_threshold, z_threshold)

df_base = load_pipeline()
df, report = run_anomaly(df_base, pf_threshold, z_threshold)

# TIME NORMALIZATION (FORMAT FIX)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# TIME FILTERING
st.sidebar.header("Time Window")

min_time = df["timestamp"].min()
max_time = df["timestamp"].max()

date_range = st.sidebar.date_input(
    "Date Range",
    [min_time, max_time]
)

if len(date_range) == 2:
    start, end = date_range
    df = df[
        (df["timestamp"] >= pd.to_datetime(start)) &
        (df["timestamp"] <= pd.to_datetime(end))
    ]

#  KPI LAYER (WINDOW-BASED SCORING)
total_records = len(df)

total_anomalies = int(df["anomaly"].sum())
anomaly_rate = total_anomalies / total_records if total_records > 0 else 0.0

system_health_score = 100 * (1 - anomaly_rate)

if system_health_score > 90:
    grid_state = "Healthy"
elif system_health_score > 75:
    grid_state = "Degraded"
else:
    grid_state = "Critical"


# DISPLAY KPI SCORECARD
c0, c1, c2, c3, c4 = st.columns(5)

c0.metric("Total Records", len(df))
c1.metric("Total Anomalies", total_anomalies)
c2.metric("Anomaly Rate", f"{anomaly_rate:.2%}")
c3.metric(
    "System Health Score",
    f"{system_health_score:.1f}/100"
)
c4.metric("Grid State", grid_state)

st.divider()

# EVENT LOG
st.subheader("Anomaly Data Logs")

event_df = df[df["anomaly"]].sort_values("timestamp", ascending=True)

st.dataframe(
    event_df[
        [
            "timestamp",
            "kw_net",
            "kvar_net",
            "pf",
            "kva",
            "anomaly_score",
            "severity"
        ]
    ],
    use_container_width=True
)

st.download_button(
    "Export Logs (CSV)",
    event_df.to_csv(index=False).encode("utf-8"),
    "grid_events.csv",
    "text/csv"
)

st.divider()

# VISUALIZATION LAYER
st.subheader("Active Power Flow")
fig1 = px.line(df, x="timestamp", y=["kw+", "kw-"])
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Reactive Power Flow")
fig2 = px.line(df, x="timestamp", y=["kvar+", "kvar-"])
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Power Factor Trend")
fig3 = px.line(df, x="timestamp", y="pf")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Power System State Space (P-Q Plane)")
fig4 = px.scatter(
    df,
    x="kw_net",
    y="kvar_net",
    color="severity",
    opacity=0.7,
    title="Grid Operating Regions"
)

st.plotly_chart(fig4, use_container_width=True)
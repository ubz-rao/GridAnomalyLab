import numpy as np
import pandas as pd

# Anomaly Detector
def detect_anomalies(df, pf_threshold, z_threshold):

    df = df.copy()

    kw = df["kw_net"]
    kvar = df["kvar_net"]
    pf = df["pf"]


    # Z SCORE (LOAD SPIKE)
    window = 48

    rolling_mean = kw.rolling(window, min_periods=10).mean()
    rolling_std = kw.rolling(window, min_periods=10).std()

    z = (kw - rolling_mean) / (rolling_std + 1e-6)

    # ANOMALY CONDITIONS
    low_pf = pf < pf_threshold

    load_spike = np.abs(z) > z_threshold

    reactive_issue = np.abs(kvar) > 1.4 * np.maximum(np.abs(kw), 0.5)

    # SCORING (0–5)
    score = (
        low_pf.astype(int) * 1 +
        load_spike.astype(int) * 2 +
        reactive_issue.astype(int) * 2
    )

    df["anomaly_score"] = np.clip(score, 0, 5)
    df["anomaly"] = df["anomaly_score"] > 0

    # SEVERITY
    df["severity"] = pd.cut(
        df["anomaly_score"],
        bins=[-0.1, 0, 1, 3, 5],
        labels=["Normal", "Low", "Medium", "High"]
    )

    # REPORT
    report = {
        "total_records": len(df),
        "anomalies": int(df["anomaly"].sum()),
        "anomaly_rate": float(df["anomaly"].mean()),
        "severity_counts": df["severity"].value_counts().to_dict(),
        "score_distribution": {
            "0": int((df["anomaly_score"] == 0).sum()),
            "1": int((df["anomaly_score"] == 1).sum()),
            "2-3": int(((df["anomaly_score"] >= 2) & (df["anomaly_score"] <= 3)).sum()),
            "4-5": int((df["anomaly_score"] >= 4).sum()),
        }
    }

    return df, report
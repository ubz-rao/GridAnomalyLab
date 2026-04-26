import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd


# POWER TREND
def plot_multi_power_trend(df, output_dir):

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    # 1 hourly aggregation for clarity
    hourly = df.resample("1h").mean(numeric_only=True)

    plt.figure(figsize=(14, 6))

    plt.plot(hourly.index, hourly["kw+"], label="Import kW", linewidth=1.5)
    plt.plot(hourly.index, hourly["kw-"], label="Export kW", linewidth=1.25)
    plt.plot(hourly.index, hourly["kvar+"], label="Import kVAR", linewidth=1.0)
    plt.plot(hourly.index, hourly["kvar-"], label="Export kVAR", linewidth=0.75)

    plt.title("Active & Reactive Power Profile (Import vs Export)")
    plt.xlabel("Time")
    plt.ylabel("Power")
    plt.grid(alpha=0.25)
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "power_trend.png"), dpi=300)
    plt.close()


# POWER QUADRANT
def plot_quadrant(df, output_dir):

    x = df["kw_net"].values
    y = df["kvar_net"].values

    anomaly_mask = df["anomaly_score"] > 0

    plt.figure(figsize=(8, 8))

    # NORMAL READS
    plt.hist2d(
        x,
        y,
        bins=100,
        cmap="Blues",
        cmin=1,
        alpha=0.95
    )

    # ANOMALIES
    plt.scatter(
        x[anomaly_mask],
        y[anomaly_mask],
        c="red",
        s=12,
        edgecolors="black",
        linewidths=0.3,
        label="Anomalies",
        zorder=3
    )

    plt.axhline(0, color="black", linewidth=1)
    plt.axvline(0, color="black", linewidth=1)

    max_val = max(abs(x).max(), abs(y).max()) * 1.05
    plt.xlim(-max_val, max_val)
    plt.ylim(-max_val, max_val)

    plt.gca().set_aspect("equal", adjustable="box")

    plt.title("Power Quadrant Distribution with Anomaly Detection")
    plt.xlabel("Net Active Power (kW)")
    plt.ylabel("Net Reactive Power (kVAR)")
    plt.grid(alpha=0.15)

    plt.legend(loc="upper right")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "quadrant.png"), dpi=300)
    plt.close()


# POWER FACTOR PLOT
def plot_power_factor(df, output_dir):

    pf = df["pf"].clip(0, 1)

    plt.figure(figsize=(14, 5))

    plt.plot(df["timestamp"], pf, linewidth=1.0, label="Power Factor")

    plt.ylim(0, 1.05)

    # REFERENCE LINES
    plt.axhline(0.9, linestyle="--", color="green", label="Good (0.9)")
    plt.axhline(0.7, linestyle="--", color="orange", label="Warning (0.7)")

    # highlight low PF regions
    plt.fill_between(
        df["timestamp"],
        0,
        1,
        where=(pf < 0.7),
        color="red",
        alpha=0.08
    )

    plt.title("Power Factor Compliance & Stability Analysis")
    plt.xlabel("Time")
    plt.ylabel("Power Factor")
    plt.grid(alpha=0.25)
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "power_factor.png"), dpi=300)
    plt.close()


# LOAD STRESS
def plot_load_stress(df, output_dir):

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    d = df.resample("1h").mean(numeric_only=True)
    kva = d["kva"]

    threshold = np.percentile(kva, 95)

    plt.figure(figsize=(14, 5))

    plt.plot(d.index, kva, color="purple", linewidth=2, label="kVA")

    plt.axhline(threshold, linestyle="--", color="red", label="95th Percentile")

    plt.fill_between(
        d.index,
        threshold,
        kva.max(),
        color="red",
        alpha=0.1
    )

    plt.title("Apparent Power Demand with Stress Threshold (95th Percentile)")
    plt.xlabel("Time")
    plt.ylabel("Apparent Power (kVA)")
    plt.grid(alpha=0.25)
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "load_stress.png"), dpi=300)
    plt.close()
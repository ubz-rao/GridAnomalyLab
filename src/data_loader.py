import pandas as pd
import numpy as np


# Dummy Data Generator
def generate_dummy(start="2026-01-01", days=90, freq="30min"):
    rng = np.random.default_rng()

    ts = pd.date_range(start=start, periods=days * 48, freq=freq)
    n = len(ts)

    hour = ts.hour.to_numpy()
    dow = ts.dayofweek.to_numpy()

    # LOAD PROFILE
    morning_peak = np.exp(-((hour - 8) ** 2) / 10)
    evening_peak = np.exp(-((hour - 19) ** 2) / 12)

    base_load = 1.4 + 2.0 * (morning_peak + evening_peak)

    weekend_factor = np.where(dow >= 5, 0.75, 1.0)
    drift = 1 + 0.03 * np.sin(2 * np.pi * np.arange(n) / (48 * 20))

    net_demand = base_load * weekend_factor * drift

    noise = rng.normal(0, 0.15, n)
    noise = np.convolve(noise, np.ones(5) / 5, mode="same")

    net_demand = np.clip(net_demand + noise, 0, None)

    # SOLAR MODEL
    solar_curve = np.maximum(0, np.sin((hour - 6) / 12 * np.pi))

    # PV penetration
    pv_generation = 1.15 * solar_curve * (1 + rng.normal(0, 0.05, n))
    pv_generation = np.clip(pv_generation, 0, None)

    # Self-consumption
    self_consumption_ratio = 0.20 + 0.20 * solar_curve

    self_consumed = pv_generation * self_consumption_ratio

    # GRID FLOW LOGIC
    grid_import = net_demand - self_consumed
    grid_export = pv_generation - self_consumed

    # Ensure no negative export/import
    grid_import = np.clip(grid_import, 0, None)
    grid_export = np.clip(grid_export, 0, None)

    # OPERATIONAL VARIABILITY
    grid_import += rng.normal(0, 0.12, n)
    grid_export += rng.normal(0, 0.10, n)

    grid_import = np.clip(grid_import, 0, None)
    grid_export = np.clip(grid_export, 0, None)

    # REACTIVE POWER
    kvar_import = 0.55 * grid_import + rng.normal(0, 0.15, n)
    kvar_export = 0.40 * grid_export + rng.normal(0, 0.12, n)

    kvar_import = np.clip(kvar_import, 0, None)
    kvar_export = np.clip(kvar_export, 0, None)

    return pd.DataFrame({
        "timestamp": ts,
        "kw+": grid_import,
        "kw-": grid_export,
        "kvar+": kvar_import,
        "kvar-": kvar_export
    })


# Loading real data
def load_data(use_dummy, csv_file):
    if use_dummy:
        return generate_dummy()

    df = pd.read_csv(csv_file, parse_dates=["timestamp"])
    df.columns = df.columns.str.strip()
    return df
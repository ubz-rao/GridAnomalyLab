import os
import json
import logging

from src.data_loader import load_data
from src.features import create_features
from src.anomaly import detect_anomalies
from src.visualization import (
    plot_quadrant,
    plot_multi_power_trend,
    plot_power_factor,
    plot_load_stress
)

logging.basicConfig(level=logging.INFO, format="%(message)s")


# PIPELINE
def run_pipeline(config):

    output_dir = config["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    # LOAD DATA
    logging.info("Loading data")
    df = load_data(config["use_dummy"], config["csv_file"])

    if df is None or df.empty:
        raise ValueError("Dataset is empty")

    # FEATURE ENGINEERING
    logging.info("Feature engineering")
    df = create_features(df)

    # ANOMALY DETECTION
    logging.info("Detecting anomalies")

    df, report = detect_anomalies(
        df,
        config["pf_threshold"],
        config["z_threshold"]
    )

    logging.info(f"Anomalies detected: {report['anomalies']}")

    # VISUALIZATION
    logging.info("Generating visualizations")

    plot_multi_power_trend(df, output_dir)
    plot_quadrant(df, output_dir)
    plot_power_factor(df, output_dir)
    plot_load_stress(df, output_dir)

    # EXPORT DATA + REPORT
    logging.info("Exporting results")

    df.to_csv(os.path.join(output_dir, "processed.csv"), index=False)

    with open(os.path.join(output_dir, "report.json"), "w") as f:
        json.dump(report, f, indent=4)

    logging.info("Pipeline completed successfully")
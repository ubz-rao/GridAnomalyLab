import numpy as np
import pandas as pd

# Feature Extractor
def create_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # NET POWER
    df["kw_net"] = df["kw+"] - df["kw-"]
    df["kvar_net"] = df["kvar+"] - df["kvar-"]

    # APPARENT POWER
    df["kva"] = np.sqrt(df["kw_net"]**2 + df["kvar_net"]**2)

    # POWER FACTOR
    df["pf"] = np.divide(
        np.abs(df["kw_net"]),
        df["kva"],
        out=np.zeros(len(df)),
        where=df["kva"] > 1e-9
    )

    df["pf"] = np.clip(df["pf"], 0, 1)

    return df
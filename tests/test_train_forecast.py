"""Test smoke del módulo de forecast."""
from src.ml.train_forecast import engineer_features
import pandas as pd


def test_engineer_features_adds_temporal_columns():
    df = pd.DataFrame({
        "Date": pd.to_datetime(["2010-02-05", "2010-02-12"]),
        "Store": [1, 1],
        "Type": ["A", "A"],
        "CPI": [1.0, 1.0],
        "Unemployment": [8.0, 8.1],
        "MarkDown1": [None, None],
        "MarkDown2": [None, None],
        "MarkDown3": [None, None],
        "MarkDown4": [None, None],
        "MarkDown5": [None, None],
    })
    out = engineer_features(df)
    assert "Year" in out.columns
    assert "Month" in out.columns
    assert "Week" in out.columns
    assert out["MarkDown1"].isna().sum() == 0

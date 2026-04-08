"""Train a scoring-average prediction model using seeded player stats.

Compares a LinearRegression baseline against a RandomForestRegressor.
Saves the better model artifact and evaluation metrics.
"""

import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.player_stat import PlayerStat

ARTIFACT_DIR = "/app/ml_artifacts"
METRICS_PATH = os.path.join(ARTIFACT_DIR, "metrics.json")
MODEL_PATH = os.path.join(ARTIFACT_DIR, "scoring_model.joblib")

FEATURE_WINDOW = 3


def load_data() -> pd.DataFrame:
    """Pull player_stats from the database into a DataFrame."""
    db = SessionLocal()
    try:
        stmt = select(PlayerStat).order_by(PlayerStat.player_id, PlayerStat.event_date)
        rows = db.scalars(stmt).all()
        data = [
            {
                "player_id": r.player_id,
                "event_date": r.event_date,
                "scoring_average": float(r.scoring_average) if r.scoring_average else None,
                "strokes_gained_total": float(r.strokes_gained_total) if r.strokes_gained_total else None,
                "driving_accuracy": float(r.driving_accuracy) if r.driving_accuracy else None,
                "greens_in_regulation": float(r.greens_in_regulation) if r.greens_in_regulation else None,
                "putting_average": float(r.putting_average) if r.putting_average else None,
            }
            for r in rows
        ]
        return pd.DataFrame(data)
    finally:
        db.close()


def build_features(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Create sliding-window features from per-player stat histories.

    For each player, uses the mean of the previous FEATURE_WINDOW events
    as features to predict the next scoring_average.
    """
    X_list, y_list = [], []
    for _, group in df.groupby("player_id"):
        group = group.sort_values("event_date").dropna(subset=["scoring_average"])
        if len(group) < FEATURE_WINDOW + 1:
            continue
        for i in range(FEATURE_WINDOW, len(group)):
            window = group.iloc[i - FEATURE_WINDOW : i]
            target = group.iloc[i]["scoring_average"]
            features = [
                window["scoring_average"].mean(),
                window["strokes_gained_total"].mean(),
                window["driving_accuracy"].mean(),
                window["greens_in_regulation"].mean(),
                window["putting_average"].mean(),
            ]
            X_list.append(features)
            y_list.append(target)
    return np.array(X_list), np.array(y_list)


def train():
    print("Loading data from database...")
    df = load_data()
    print(f"  {len(df)} stat rows loaded across {df['player_id'].nunique()} players")

    print("Building features...")
    X, y = build_features(df)
    print(f"  {len(X)} training samples created (window={FEATURE_WINDOW})")

    if len(X) < 10:
        print("ERROR: Not enough data to train. Run 'make seed' first.")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Baseline: LinearRegression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    lr_rmse = float(np.sqrt(mean_squared_error(y_test, lr_pred)))
    lr_mae = float(mean_absolute_error(y_test, lr_pred))

    # Improved: RandomForestRegressor
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_rmse = float(np.sqrt(mean_squared_error(y_test, rf_pred)))
    rf_mae = float(mean_absolute_error(y_test, rf_pred))

    print("\n── Model Comparison ────────────────────────")
    print(f"  LinearRegression  — RMSE: {lr_rmse:.4f}  MAE: {lr_mae:.4f}")
    print(f"  RandomForest      — RMSE: {rf_rmse:.4f}  MAE: {rf_mae:.4f}")

    # Pick the better model
    chosen_name = "RandomForestRegressor" if rf_rmse <= lr_rmse else "LinearRegression"
    chosen_model = rf if rf_rmse <= lr_rmse else lr
    chosen_rmse = rf_rmse if rf_rmse <= lr_rmse else lr_rmse
    chosen_mae = rf_mae if rf_rmse <= lr_rmse else lr_mae
    print(f"\n  Winner: {chosen_name}")

    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    joblib.dump(chosen_model, MODEL_PATH)
    print(f"  Model saved → {MODEL_PATH}")

    metrics = {
        "chosen_model": chosen_name,
        "chosen_rmse": round(chosen_rmse, 4),
        "chosen_mae": round(chosen_mae, 4),
        "baseline": {
            "model": "LinearRegression",
            "rmse": round(lr_rmse, 4),
            "mae": round(lr_mae, 4),
        },
        "improved": {
            "model": "RandomForestRegressor",
            "rmse": round(rf_rmse, 4),
            "mae": round(rf_mae, 4),
        },
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "feature_window": FEATURE_WINDOW,
        "features": [
            "avg_scoring_average",
            "avg_strokes_gained_total",
            "avg_driving_accuracy",
            "avg_greens_in_regulation",
            "avg_putting_average",
        ],
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"  Metrics saved → {METRICS_PATH}")

    print("\nTraining complete ✓")


if __name__ == "__main__":
    train()

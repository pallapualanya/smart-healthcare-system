"""
predictive_model.py
Two pieces of "predictive analytics" over patient vitals:

1. Anomaly detection using an Isolation Forest — flags readings that look
   statistically unusual compared to a baseline of normal vitals.
2. Simple trend forecasting using linear regression — predicts where a
   vital sign is heading over the next few readings, so caregivers get
   an early warning rather than just a snapshot.
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

VITAL_KEYS = ["heart_rate", "systolic_bp", "diastolic_bp", "oxygen_saturation", "temperature_c"]


class AnomalyDetector:
    def __init__(self, baseline_samples=200):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self._fit_on_synthetic_baseline(baseline_samples)

    def _fit_on_synthetic_baseline(self, n):
        rng = np.random.default_rng(42)
        baseline = np.column_stack([
            rng.normal(75, 5, n),    # heart_rate
            rng.normal(118, 6, n),   # systolic_bp
            rng.normal(78, 5, n),    # diastolic_bp
            rng.normal(97.5, 0.8, n),  # oxygen_saturation
            rng.normal(36.8, 0.2, n),  # temperature_c
        ])
        self.model.fit(baseline)

    def check(self, reading: dict) -> dict:
        vector = np.array([[reading[k] for k in VITAL_KEYS]])
        prediction = self.model.predict(vector)[0]  # 1 = normal, -1 = anomaly
        score = self.model.decision_function(vector)[0]  # lower = more anomalous
        return {
            "is_anomaly": bool(prediction == -1),
            "anomaly_score": round(float(score), 4),
        }


class TrendForecaster:
    """Predicts the next value of a vital sign from a short recent history."""

    def forecast(self, history: list, steps_ahead: int = 3) -> float | None:
        if len(history) < 4:
            return None
        X = np.arange(len(history)).reshape(-1, 1)
        y = np.array(history)
        model = LinearRegression().fit(X, y)
        next_x = np.array([[len(history) + steps_ahead - 1]])
        prediction = model.predict(next_x)[0]
        return round(float(prediction), 1)

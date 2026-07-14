"""
app.py
Flask backend for the Smart Healthcare System.

Serves:
- GET  /                -> the caregiver dashboard (HTML)
- GET  /api/reading      -> a new simulated vitals reading, with anomaly
                             detection and a short-term trend forecast

Run with:
    python backend/app.py
Then open http://localhost:5000 in your browser.
"""

import os
from collections import deque

from flask import Flask, jsonify, send_from_directory

from vitals_simulator import VitalsSimulator
from predictive_model import AnomalyDetector, TrendForecaster, VITAL_KEYS

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)

simulator = VitalsSimulator()
detector = AnomalyDetector()
forecaster = TrendForecaster()

# keep a short rolling history per vital for trend forecasting
history = {key: deque(maxlen=20) for key in VITAL_KEYS}


@app.route("/")
def dashboard():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/api/reading")
def get_reading():
    reading = simulator.get_reading()

    for key in VITAL_KEYS:
        history[key].append(reading[key])

    anomaly_result = detector.check(reading)

    forecasts = {
        key: forecaster.forecast(list(history[key]))
        for key in VITAL_KEYS
    }

    return jsonify({
        "reading": reading,
        "anomaly": anomaly_result,
        "forecast": forecasts,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)

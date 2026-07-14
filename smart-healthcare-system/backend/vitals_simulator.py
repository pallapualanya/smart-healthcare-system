"""
vitals_simulator.py
Simulates real-time patient vitals (heart rate, blood pressure, oxygen
saturation, temperature) for demo purposes, since we don't have a live
patient monitor to connect to. Occasionally injects an anomaly so the
detection system has something to catch.
"""

import random
import time


class VitalsSimulator:
    def __init__(self, patient_id="P001", anomaly_chance=0.12):
        self.patient_id = patient_id
        self.anomaly_chance = anomaly_chance
        self.tick = 0

    def _normal_reading(self):
        return {
            "heart_rate": round(random.gauss(75, 5), 1),
            "systolic_bp": round(random.gauss(118, 6), 1),
            "diastolic_bp": round(random.gauss(78, 5), 1),
            "oxygen_saturation": round(random.gauss(97.5, 0.8), 1),
            "temperature_c": round(random.gauss(36.8, 0.2), 1),
        }

    def _anomalous_reading(self):
        anomaly_type = random.choice(["tachycardia", "hypoxia", "fever", "hypotension"])
        reading = self._normal_reading()
        if anomaly_type == "tachycardia":
            reading["heart_rate"] = round(random.uniform(120, 160), 1)
        elif anomaly_type == "hypoxia":
            reading["oxygen_saturation"] = round(random.uniform(82, 90), 1)
        elif anomaly_type == "fever":
            reading["temperature_c"] = round(random.uniform(38.5, 40.0), 1)
        elif anomaly_type == "hypotension":
            reading["systolic_bp"] = round(random.uniform(75, 89), 1)
        reading["_injected_anomaly"] = anomaly_type
        return reading

    def get_reading(self):
        self.tick += 1
        is_anomaly = random.random() < self.anomaly_chance
        reading = self._anomalous_reading() if is_anomaly else self._normal_reading()
        reading["patient_id"] = self.patient_id
        reading["tick"] = self.tick
        reading["timestamp"] = time.time()
        return reading

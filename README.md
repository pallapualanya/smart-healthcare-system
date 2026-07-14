# Smart Healthcare System

An AI-powered system that monitors patient health data in real time, using machine learning to forecast patient conditions and detect anomalies — paired with a clean web dashboard for caregivers.

## Overview

This project was built to explore how predictive analytics can support proactive patient care rather than purely reactive monitoring. It ingests patient vitals, runs them through a trained model to flag potential issues early, and presents the results through a simple, readable dashboard.

## Features

- **Real-time monitoring** of patient health metrics
- **Predictive analytics** to forecast patient condition trends
- **Anomaly detection** to flag unusual readings that may need attention
- **Caregiver dashboard** built with HTML/CSS for clear, at-a-glance visibility

## Tech Stack

- **Language:** Python
- **Machine Learning:** scikit-learn / Python-based ML libraries for predictive modeling
- **Frontend:** HTML, CSS
- **Data Handling:** Structured patient vitals data (e.g., heart rate, blood pressure, oxygen levels)

## How It Works

1. Patient health data is collected (simulated or input-based, depending on setup)
2. The data is passed through a trained ML model that evaluates trends over time
3. The model flags anomalies or predicts potential complications
4. Results are displayed on a caregiver-facing dashboard for quick interpretation

## What I Learned

- Structuring a real-time-style data pipeline from ingestion to visualization
- Applying predictive analytics to a practical, high-stakes domain (healthcare)
- Designing a simple frontend that communicates model outputs clearly to non-technical users (caregivers)

## Possible Future Improvements

- Connect to real wearable device APIs for live data instead of simulated input
- Add historical trend charts for each patient
- Introduce alert thresholds configurable by medical staff
- Expand the model to handle multiple condition types simultaneously

## Author

Alanya Pallapu — Computer Science Engineering, MRCET, Hyderabad

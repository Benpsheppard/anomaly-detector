# Anomaly Detector - Python
A real-time anomaly detection web app built in Python using Streamlit. It continuously generates and visualizes time-series data, detecting and highlighting anomalies in real-time.

## Features
 - Personalised data generation methods
 - Personalised anomaly detection methods
 - Chart displaying data in real-time
 - Anomalies detected and presented to the user in real-time

## Installation
Clone the repo:
```bash
git clone https://github.com/Benpsheppard/anomaly-detector.git
cd anomaly-detector
```
Create and activate virtual environment:
```bash
python -m venv venv
venv/Scripts/activate
```
Download requirements inside the virtual environment (venv):
```bash
pip install -r requirements.txt
```
Run the app:
```bash
streamlit run App.py
```
- Streamlit will open in your default web browser

## Tech Stack
- Python
- Streamlit Web UI

## Libraries used
- Streamlit - UI
- Time - rerunning data generation loop
- Datetime - timestamps
- Collections - deque for managing data points
- Plotly - data chart
- Numpy - mathematics
- Scipy - grubbs test calculation
- Random - inserting random anomalies

## Usage
- Select a data generation method from the sidebar drop-down menu
- Select an anomaly detection method from the sidebar drop-down menu
- Configure your settings using the sliders provided
- Start / Stop / Reset data generation using buttons provided in the sidebar
- Watch the program in real-time detect simulated anomalies within the data on a chart

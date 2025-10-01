## Imports
import streamlit as st
import time
import numpy as np
import random
from datetime import datetime
from collections import deque
import plotly.graph_objects as go

# Import files
import AnomalyDetectors as ad
import DataGenerators as dg

## Page config
st.set_page_config(
    page_title="Anomaly Detector", 
    layout="wide"
)

## Initialize session state
if "data" not in st.session_state:
    # Store last 2oo data points
    st.session_state.data = deque(maxlen=200)
    st.session_state.timestamps = deque(maxlen=200)
    st.session_state.anomalies = deque(maxlen=200)

    # If app is actively running
    st.session_state.is_running = False

    # Counters
    st.session_state.data_points = 0
    st.session_state.anomaly_count = 0

    # When streaming started
    st.session_state.start_time = datetime.now()

## Create chart
def create_chart(data, timestamps, anomalies):
    fig = go.Figure()

    # Line
    fig.add_trace(go.Scatter(
        x=timestamps, y=data,
        mode="lines+markers",
        line=dict(color="white"),
        marker=dict(size=6, color="white"),
        name="Data"
    ))

    # Anomalies
    anomaly_indices = [i for i, a in enumerate(anomalies) if a]
    if anomaly_indices:
        fig.add_trace(go.Scatter(
            x=[timestamps[i] for i in anomaly_indices],
            y=[data[i] for i in anomaly_indices],
            mode="markers",
            marker=dict(size=12, color="red", symbol="x"),
            name="Anomaly"
        ))

    fig.update_layout(
        title="Anomaly Detection",
        xaxis_title="Time",
        yaxis_title="Value",
        template="plotly_dark",
        height=500
    )
    return fig

## Generate data point
def generate_data_point(data_type):

    # List of different generator types
    generators = {
        "Stock Price": lambda: dg.stock_price(),
        "Temperature Readings": lambda: dg.temp_sensor_readings()
    }

    value = generators[data_type]()

    return value

## Check for anomaly
def detect_anomaly(data, method, **params):

    # List of different detection methods
    detectors = {
        "Z-score": lambda: ad.z_score(list(data), params.get('threshold', 3)),
        "InterQuartile Range": lambda: ad.iqr(list(data), params.get('multiplier', 1.5))
    }

    return detectors[method]()

## Sidebar controls and layout
st.sidebar.title("Controls")

## Drop down menu for picking data generation type
data_type = st.sidebar.selectbox(
    "Data Generator", 
    ["Stock Price", "Temperature Readings"], 
    help="Select the type of data to generate"
)

## Drop down menu for picking anomaly detection method
detection_method = st.sidebar.selectbox(
    "Detection Method",
    ["Z-score", "InterQuartile Range"],
    help="Select an Anomaly Detection method"
)

# Sidebar subheader for params
st.sidebar.subheader("Algorithm Parameters")
params = {}

## Checks which detection method is being used
if (detection_method == "Z-score"):
    params['threshold'] = st.sidebar.slider("Z-score Threshold", 1.0, 5.0, 2.5, 1.0)

elif (detection_method == "InterQuartile Range"):
    params['multiplier'] = st.sidebar.slider("IQR Multiplier", 1.0, 3.0, 1.5, 0.1)

# Speed at which points are generated
update_speed = st.sidebar.slider("Update Speed", 1, 10, 5)      

## Button layout
col1, col2 = st.sidebar.columns(2)
start_button = col1.button("Start")
stop_button = col2.button("Stop")
reset_button = st.sidebar.button("Reset")

## Button logic
if start_button:
    st.session_state.is_running = True
if stop_button:
    st.session_state.is_running = False
if reset_button:
    st.session_state.data.clear()
    st.session_state.timestamps.clear()
    st.session_state.anomalies.clear()
    st.session_state.data_points = 0
    st.session_state.anomaly_count = 0
    st.session_state.start_time = datetime.now()
    st.rerun()

## Show Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Data Points", st.session_state.data_points)
col2.metric("Anomalies", st.session_state.anomaly_count)
rate = (st.session_state.anomaly_count / st.session_state.data_points * 100) if st.session_state.data_points > 0 else 0
col3.metric("Anomaly Rate", f"{rate:.2f}%")

# Chart Placeholder
chart_placeholder = st.empty()

## Streaming loop
if st.session_state.is_running:

    # Generate value with timestamp
    value = generate_data_point(data_type)
    current_time = datetime.now()

    # Add value to session data
    st.session_state.data.append(value)
    st.session_state.timestamps.append(current_time)
    st.session_state.data_points += 1

    # Detect Anomaly
    is_anomaly = False
    if len(st.session_state.data) > 10:
        is_anomaly = detect_anomaly(st.session_state.data, detection_method, **params) 

    # Add anomaly to list and increase anomaly counter
    st.session_state.anomalies.append(is_anomaly)
    if is_anomaly:
        st.session_state.anomaly_count += 1
        st.toast(f"Anomaly detected! Value: {value:.2f} at {current_time.strftime('%H:%M:%S')}")

    # Update chart with data and put in placeholder
    fig = create_chart(
        list(st.session_state.data),
        list(st.session_state.timestamps),
        list(st.session_state.anomalies)
    )
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # Rerun loop
    time.sleep(1 / update_speed)
    st.rerun()

else:
    # Show current paused data state
    if st.session_state.data:
        fig = create_chart(
            list(st.session_state.data),
            list(st.session_state.timestamps),
            list(st.session_state.anomalies)
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Click 'Start' to begin streaming data")

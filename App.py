''' File for handling streamlit and main app functionality '''

## Imports
import streamlit as st
import time
from datetime import datetime
from collections import deque

# Import files
import AnomalyDetectors as ad
import DataGenerators as dg
import Chart as ch

## Page config
st.set_page_config(
    page_title="Anomaly Detector", 
    layout="wide"
)

## Import CSS
def load_css(file_name):
    with open(file_name) as f:
        css = f"<style>div[data-testid='stAppViewContainer'] {{{f.read()}}}</style>"
        st.markdown(css, unsafe_allow_html=True)
load_css("style.css")

## Initialize session state
if "data" not in st.session_state:
    # Store last 200 data points
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

## Sidebar controls and layout
st.sidebar.title("Controls")

## Drop down menu for picking data generation type
data_type = st.sidebar.selectbox(
    "Data Generator", 
    ["Stock Price", "Temperature Readings", "Network Traffic", "Sinusoidal Wave"], 
    help="Select the type of data to generate"
)

## Drop down menu for picking anomaly detection method
detection_method = st.sidebar.selectbox(
    "Detection Method",
    ["Z-score", "InterQuartile Range", "Rolling Z-score", "Grubbs' Test"],
    help="Select an Anomaly Detection method"
)

# Sidebar subheader for params
st.sidebar.subheader("Algorithm Parameters")
params = {}

# Get detector specific parameters
match detection_method:
    case "Z-score":
        params['threshold'] = st.sidebar.slider("Z-score Threshold", 1.0, 5.0, 2.0, 1.0)
    case "InterQuartile Range":
        params['multiplier'] = st.sidebar.slider("IQR Multiplier", 1.0, 3.0, 2.0, 0.1)
    case "Rolling Z-score":
        params['window'] = st.sidebar.slider("Rolling Z-score Window", 5, 50, 25, 5)
        params['threshold'] = st.sidebar.slider("Rolling Z-score Threshold", 1.0, 5.0, 3.0, 1.0)
    case "Grubbs' Test":
        params['alpha'] = st.sidebar.slider("Grubbs' Test Alpha", 0.01, 0.3, 0.05, 0.01)

# Speed at which points are generated
update_speed = st.sidebar.slider("Update Speed", 1, 10, 5)      

## Button layout
start_button = st.sidebar.button("Start")
stop_button = st.sidebar.button("Stop")
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
    st.session_state.is_running = False
    st.rerun()

## Main app layout
st.title("Real-Time Anomaly Detection Simulation")
st.markdown("""
            <div>
                <p style="font-size:16px;">Simulate streaming data and detect anomalies using various algorithms.</p>
            </div>
            """, unsafe_allow_html=True)

# System status
if st.session_state.is_running:
    st.success("System Status: Running - Generating data in real-time")
else:
    st.info("System Status: Paused - Click 'Start' to begin generating data")

# Updated Placeholders
metric_placeholder = st.empty()
chart_placeholder = st.empty()

## Streaming loop
if st.session_state.is_running:
    # Generate value with timestamp
    t = st.session_state.data_points
    value = dg.generate_data_point(data_type, t)
    current_time = datetime.now()

    # Add value to session data
    st.session_state.data.append(value)
    st.session_state.timestamps.append(current_time)
    st.session_state.data_points += 1

    # Detect Anomaly
    is_anomaly = False
    if len(st.session_state.data) > 10:
        is_anomaly = ad.detect_anomaly(st.session_state.data, detection_method, **params) 

    # Add anomaly to list and increase anomaly counter
    st.session_state.anomalies.append(is_anomaly)
    if is_anomaly:
        st.session_state.anomaly_count += 1
        st.toast(f"Anomaly detected! Value: {value:.2f} at {current_time.strftime('%H:%M:%S')}")

    # Update Metrics
    with metric_placeholder.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Data Points", st.session_state.data_points)
        col2.metric("Anomalies", st.session_state.anomaly_count)
        rate = (st.session_state.anomaly_count / st.session_state.data_points * 100) if st.session_state.data_points > 0 else 0
        col3.metric("Anomaly Rate", f"{rate:.2f}%")
        col4.metric("Elapsed Time", (datetime.now() - st.session_state.start_time).seconds)

    # Update chart with data and put in placeholder
    fig = ch.create_chart(
        list(st.session_state.data),
        list(st.session_state.timestamps),
        list(st.session_state.anomalies),
        data_type
    )
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # Rerun loop
    time.sleep(1 / update_speed)
    st.rerun()

else:
    # Show current paused data state
    if st.session_state.data:
        fig = ch.create_chart(
            list(st.session_state.data),
            list(st.session_state.timestamps),
            list(st.session_state.anomalies),
            data_type
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Click 'Start' to begin streaming data")

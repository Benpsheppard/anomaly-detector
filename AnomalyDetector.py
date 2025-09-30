## Imports
import streamlit as st
import time
import numpy as np
import random
from datetime import datetime
from collections import deque
import plotly.graph_objects as go

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

## Simulated stock prices
def stock_price(base_price=100, volatility=2): 
    change = np.random.normal(0, volatility)            # Generate random change in price using volatility setting

    # Inject anomalies
    if random.random() < 0.05:          # 5% chance of anomaly
        change *= random.choice([3, -3, 4, -4])         # Multiple change by random option in list (values selected for obvious spikes/dips)

    return base_price + change      # Change price of stock by calculated change


## Z-Score Anomaly Detection
def z_score(data, threshold=3):             # Takes data and sets threshold to default value
    if len(data) < 3:       # Checks there is enough data
        return False  
        
    mean = np.mean(data)        # Calculates mean of data
    std = np.std(data)          # Calculates standard deviation of data
    if std == 0:            # Ensure std isn't zero to avoid division by zero
        return False
    
    z_score = abs((data[-1] - mean) / std)          # Calculate Z-score
    return z_score > threshold          # Return true if last data point was an anomaly


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

## Sidebar controls and layout
st.sidebar.title("Controls")

col1, col2 = st.sidebar.columns(2)
start_button = col1.button("Start")
stop_button = col2.button("Stop")
reset_button = st.sidebar.button("Reset")

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

## Chart Placeholder
chart_placeholder = st.empty()

## Streaming loop
if st.session_state.is_running:
    value = stock_price()
    current_time = datetime.now()

    st.session_state.data.append(value)
    st.session_state.timestamps.append(current_time)
    st.session_state.data_points += 1

    is_anomaly = z_score(list(st.session_state.data))
    st.session_state.anomalies.append(is_anomaly)
    if is_anomaly:
        st.session_state.anomaly_count += 1
        st.warning(f"Anomaly detected! Value: {value:.2f} at {current_time.strftime('%H:%M:%S')}")

    fig = create_chart(
        list(st.session_state.data),
        list(st.session_state.timestamps),
        list(st.session_state.anomalies)
    )
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    time.sleep(0.5)
    st.rerun()
else:
    if st.session_state.data:
        fig = create_chart(
            list(st.session_state.data),
            list(st.session_state.timestamps),
            list(st.session_state.anomalies)
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Click 'Start' to begin streaming data")

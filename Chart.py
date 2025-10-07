''' File to handle chart creation '''

## Imports
import plotly.graph_objects as go

'''
Create line chart with anomalies highlighted

@param1 data: List of data points
@param2 timestamps: List of timestamps for data points
@param3 anomalies: List of booleans indicating if data point is an anomaly
'''
def create_chart(data, timestamps, anomalies, data_type):
    fig = go.Figure()

    # Convert to lists
    data_list = list(data)
    timestamps_list = list(timestamps)
    anomalies_list = list(anomalies)

    # Lines
    for i in range(1, len(data_list)):
        color = 'green' if data_list[i] >= data_list[i-1] else 'red'        # Green for increase, red for decrease
        fig.add_trace(go.Scatter(
            x=[timestamps_list[i-1], timestamps_list[i]], 
            y=[data_list[i-1], data_list[i]],
            mode="lines",
            line=dict(color=color, width=3),
            showlegend=False    
        ))
    
    # Normal points
    fig.add_trace(go.Scatter(
        x=timestamps_list,
        y=data_list,
        mode="markers",
        marker=dict(size=6, color="#FFFFF0"),
        name="Data Points"
    ))

    # Anomaly points
    anomaly_indices = [i for i, is_anomaly in enumerate(anomalies_list) if is_anomaly]
    if anomaly_indices:
        fig.add_trace(go.Scatter(
            x=[timestamps[i] for i in anomaly_indices],
            y=[data[i] for i in anomaly_indices],
            mode="markers",
            marker=dict(size=12, color="red", symbol="x"),      # Red X for anomalies
            name="Anomaly"
        ))

    import numpy as np

    # Rolling mean line
    window = 10
    if len(data_list) > window:
        rolling_mean = np.convolve(data_list, np.ones(window)/window, mode='valid')
        fig.add_trace(go.Scatter(
            x=timestamps_list[window-1:], 
            y=rolling_mean, 
            mode="lines",
            line=dict(color="rgba(0, 255, 255, 0.3)", width=1.2),
            name="Rolling Mean"
        ))

    # Chart layout
    fig.update_layout(
        # Title Styling
        title=dict(
            text=f"{data_type} Anomaly Detection"
        ),

        # Axis labels
        xaxis_title="Time",
        yaxis_title="Value",
        plot_bgcolor="#1a1d29",
        template="plotly_dark",
        font=dict(size=14, color="#FFFFF0"),
        height=500,

        # X axis styling
        xaxis=dict(
            showgrid=True,
            gridcolor="#333333",
            zeroline=False,
            showline=True,
            linecolor="#333333",
            ticks="outside",
            tickfont=dict(size=12, color="#AAAAAA")
        ),

        # Y axis styling
        yaxis=dict(
            showgrid=True,
            gridcolor="#333333",
            zeroline=False,
            showline=True,
            linecolor="#333333",
            ticks="outside",
            tickfont=dict(size=12, color="#AAAAAA")
        )
    )
    return fig
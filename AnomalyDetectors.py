''' File to hold anomaly detector methods '''

## Imports
import numpy as np
from scipy.stats import t

'''
Z-score Anomaly Detection

@param1 data: Data to be classified
@param2 threshold: Maximum value for normal points
'''
def z_score(data, threshold=3):             # Takes data and sets threshold to default value
    if len(data) < 3:       # Checks there is enough data
        return False  
        
    mean = np.mean(data)        # Calculates mean of data
    std = np.std(data)          # Calculates standard deviation of data
    if std == 0:            # Ensure std isn't zero to avoid division by zero
        return False
    
    z_score = abs((data[-1] - mean) / std)          # Calculate Z-score
    return z_score > threshold          # Return true if last data point was an anomaly

'''
Interquartile range Anomaly Detection

@param1 data: Data to be classified
@param2 multiplier: Value to multiply quartile values by for lower and upper bounds
'''
def iqr(data, multiplier=1.5):
    if len(data) < 4:       # Checks there is enough data
        return False
    
    q1 = np.percentile(data, 25)        # Calculate first quartile
    q3 = np.percentile(data, 75)        # Calculate third quartile

    iqr = q3 - q1       # Calculate interquartile range

    lower_bound = q1 - multiplier * iqr         # Calculate lower bound for classification
    upper_bound = q3 + multiplier * iqr         # Calculate upper bound for classification

    return data[-1] < lower_bound or data[-1] > upper_bound         # Return true if data point out of bounds

'''
Rolling Z-Score Anomaly Detection

@param1 data: Data to be classified
@param2 window: Size of window for checking data
@param3 threshold: Maximum value for normal points 

'''
def rolling_z_score(data, window=20, threshold=2):
    if len(data) < window:      # Checks there is enough data to fill window
        return False
    
    recent_data = list(data)[-window:]      # Get recent data inside window
    mean = np.mean(recent_data)         # Calculate mean of windowed data
    std = np.std(recent_data)           # Calculate standard deviation of windowed data

    if std == 0:        # Ensure std isn't 0 to avoid division by 0
        return False


    rolling_z = abs((data[-1] - mean) / std)        # Calculate rolling Z-score
    return rolling_z > threshold        # Return true if last data point was an anomaly

'''
Grubbs' Test Anomaly Detection

@params1 data: Data to be classified
@params2 alpha: Significance level - leniency for detecting anomalies
'''
def grubbs_test(data, alpha=0.05):
    n = len(data)
    if n < 3:       # Checks there is enough data
        return False
    
    mean = np.mean(data)        # Calculate mean of data
    std = np.std(data, ddof=1)      # Calculate standard deviation of data with ddof = 1

    if std == 0:        # Ensure std isn't 0 to avoid division by 0
        return False

    diffs = np.abs(list(data) - mean)     # Calculate differences between each value and the mean
    max_diff_idx = np.max(diffs)        # Find biggest difference
    G = diffs[max_diff_idx] / std   # Grubbs statistic

    # Critical value
    t_crit = t.ppf(1 - alpha / (2 * n), n - 2)
    G_crit = ((n - 1) / np.sqrt(n)) * np.sqrt(t_crit**2 / (n - 2 + t_crit**2))

    return (max_diff_idx == (n - 1)) and (G > G_crit)     # Return true if last point was an anomaly

'''
Detect anomaly in data using specified method

@param1 data: Data to be classified
@param2 method: Anomaly detection method to use
@param3 params: Additional parameters for specific methods (** to allow variable number of params)
'''
def detect_anomaly(data, method, **params):
    # List of different detection methods
    detectors = {
        "Z-score": lambda: z_score(list(data), params.get('threshold', 3)),
        "InterQuartile Range": lambda: iqr(list(data), params.get('multiplier', 1.5)),
        "Rolling Z-score": lambda: rolling_z_score(list(data), params.get('window', 20), params.get('threshold', 2)),
        "Grubbs' Test": lambda: grubbs_test(list(data), params.get('alpha', 0.05))
    }

    return detectors[method]()
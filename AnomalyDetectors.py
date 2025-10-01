''' File to hold anomaly detector methods '''

## Imports
import numpy as np

'''
Z-score Anomaly Detection

@param1 data: Data to be classified
@param2 threshold: Minimum value for normal points
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
## Interquartile range Anomaly Detection
def iqr(data, multiplier=1.5):
    if len(data) < 4:       # Checks there is enough data
        return False
    
    q1 = np.percentile(data, 25)        # Calculate first quartile
    q3 = np.percentile(data, 75)        # Calculate third quartile

    iqr = q3 - q1       # Calculate interquartile range

    lower_bound = q1 - multiplier * iqr         # Calculate lower bound for classification
    upper_bound = q3 + multiplier * iqr         # Calculate upper bound for classification

    return data[-1] < lower_bound or data[-1] > upper_bound         # Return true if data point out of bounds

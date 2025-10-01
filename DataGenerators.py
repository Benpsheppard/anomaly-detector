''' File to hold Data generation methods '''

## Imports
import numpy as np
import random

'''
Simulated Stock Price Generator

@param1 base_price: Starting point at which to generate prices
@param2 volatility: Amount price can fluctuate by normally
'''
def stock_price(base_price=100, volatility=2): 
    change = np.random.normal(0, volatility)            # Generate random change in price using volatility setting

    # Inject anomalies
    if random.random() < 0.05:          # 5% chance of anomaly
        change *= random.choice([3, -3, 4, -4])         # Multiply change by random option in list (values selected for obvious spikes)

    return base_price + change      # Change price of stock by calculated change

'''
Simulated temperature sensor readings

@param1 base_temp: Starting point at which to generate temp readings
@param2 noise: Amount temp can fluctuate by normally
'''
def temp_sensor_readings(base_temp=25, noise=0.5):
    reading = base_temp + np.random.normal(0, noise)        # Generate random change in temperature using noise setting

    # Inject anomalies
    if random.random() < 0.03:      # 3% chance of anomaly
        reading += random.choice([10, -10, 15, -8])     # Add random choice to reading (values selected for obvious spikes)

    return reading
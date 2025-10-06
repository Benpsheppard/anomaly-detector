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

''' 
Simulated network traffic data

@param1 base_rate: Base rate of network traffic
@param2 burst_prob: Probability of a traffic burst occurring
'''
def network_traffic(base_rate=1000, burst_prob=0.04):
    traffic = base_rate + np.random.normal(0, 100)      # Generate random change in traffic

    # Inject bursts
    if random.random() < burst_prob:      # % chance of burst
        traffic *= random.choice([2, 3, 0.5])         # Multiply traffic by random option in list (values selected for obvious spikes or drops)

    return traffic  # Return calculated traffic value

'''
Simulated sinosoidal wave data with noise

@param1 t: Time step to calculate value at
@param2 period: Period of the wave
@param3 noise: Amount of random noise to add to wave
'''
def sinusoidal_wave(t, period=5, noise=5):
    value = 50 * np.sin(2 * np.pi * t / period) + 100      # Generate sinosoidal wave
    value += np.random.normal(0, noise)         # Add random noise to wave

    #Inject spikes
    if random.random() < 0.04:      # 4% chance of spike
        value += random.choice([35, -35, 50])      # Add random choice to value (values selected for obvious spikes)

    return value    # Return calculated wave value

'''
Generate a data point based on selected type

@param1 data_type: Type of data to generate
@param2 t: Time step to calculate value at (used for sinusoidal wave)
'''
def generate_data_point(data_type, t):

    # List of different generator types
    generators = {
        "Stock Price": lambda: stock_price(),
        "Temperature Readings": lambda: temp_sensor_readings(),
        "Network Traffic": lambda: network_traffic(),
        "Sinusoidal Wave": lambda: sinusoidal_wave(t)
    }

    value = generators[data_type]()

    return value
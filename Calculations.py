import math
import json
import numpy as np
import pandas as pd

def calculate_total_delay(distance, sf, bw):
    total_delay = (distance / speed_of_light) + (sf * bw) / math.pow(2, sf)
    return total_delay


# Function to get SNR value for a given SF
def get_snr(sf):
    return sf_to_snr.get(sf, "Invalid Spreading Factor")


def calculate_sensitivity(bw, snr):
    sensitivity = (-174) + 10 * math.log10(1000 * bw) + snr
    return sensitivity


def calculate_link_budget(pt, gtx, grx, sensitivity):
    link_budget = pt + gtx + grx - sensitivity
    return link_budget


# Function to convert watts to dBW
def watts_to_dbw(watts):
    if watts <= 0:
        return "Power in watts must be greater than zero"
    dbw = 10 * math.log10(watts)
    return dbw


def calculate_distance(pos1, pos2):
    # Calculate the Euclidean distance between two 3D points
    return np.linalg.norm(np.array(pos1) - np.array(pos2))


# Define the mapping of Spreading Factor (SF) to SNR
sf_to_snr = {
    6: -5,
    7: -7.5,
    8: -10,
    9: -12.5,
    10: -15,
    11: -17.5,
    12: -20
}

# distance = 10  # meter
speed_of_light = 10  # c,  meter/second
sf = 10  # spreading factor, constant
bw = 10  # bandwidth in kilohertz, bit/second
snr = get_snr(sf)  # signal noise ratio, dB(decibel)
pt = 10  # transmission power, dbm
gtx = 10  # transmission antenna gain, dbi
grx = 10  # receiver antenna gain, dbi
sensitivity = calculate_sensitivity(bw, snr)  # dbm


# Load module positions and gateway position from the JSON file
with open("selected_module_positions.json", 'r') as json_file:
    selected_positions = json.load(json_file)

module_positions = selected_positions['modules']
gateway_position = selected_positions['gateway']

results = []

# Calculate distances and other metrics
for module_pos in module_positions:
    # Convert positions to numpy arrays
    module_pos_array = np.array([module_pos['x'], module_pos['y'], module_pos['z']])
    gateway_pos_array = np.array([gateway_position['x'], gateway_position['y'], gateway_position['z']])

    # Calculate distance
    distance = calculate_distance(module_pos_array, gateway_pos_array)
    delay = calculate_total_delay(distance, sf, bw)
    link_budget = calculate_link_budget(pt, gtx, grx, sensitivity)

    # Append results
    results.append({
        'Module': module_pos_array.tolist(),  # Convert numpy array back to list for JSON serialization
        'Gateway': gateway_pos_array.tolist(),  # Convert numpy array back to list for JSON serialization
        'Distance': distance,
        'Total Delay': delay,
        'Link Budget': link_budget
    })


df_results = pd.DataFrame(results)
print(df_results.head(10))



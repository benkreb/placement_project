import math


def calculate_total_delay(distance, sf, bw):
    total_delay = (distance / speed_of_light) + (sf * bw) / math.pow(2, sf)
    return total_delay


def calculate_sensitivity(bw, snr):
    sensitivity = (-174) + 10 * math.log10(1000 * bw) + snr
    return sensitivity


# Function to get SNR value for a given SF
def get_snr(sf):
    return sf_to_snr.get(sf, "Invalid Spreading Factor")


def calculate_link_budget(pt, gtx, grx, sensitivity):
    link_budget = pt + gtx + grx - sensitivity
    return link_budget


# Function to convert watts to dBW
def watts_to_dbw(watts):
    if watts <= 0:
        return "Power in watts must be greater than zero"
    dbw = 10 * math.log10(watts)
    return dbw


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

distance = 10  # meter
speed_of_light = 10  # c,  meter/second
sf = 10  # spreading factor, constant
bw = 10  # bandwidth in kilohertz, bit/second
snr = get_snr(sf)  # signal noise ratio, dB(decibel)
pt = 10  # transmission power, dbm
gtx = 10  # transmission antenna gain, dbi
grx = 10  # receiver antenna gain, dbi
sensitivity = calculate_sensitivity(bw, snr)  # dbm

d_total = calculate_total_delay(distance, sf, bw)
link_budget = calculate_link_budget(pt, gtx, grx, sensitivity)

print(d_total)
print(sensitivity)
print(link_budget)


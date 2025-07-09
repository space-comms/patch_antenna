"""
Frequency Band Database for Antenna Applications

Added by Al-Musbahi for Leeds SpaceComms
(Enhancement to original library by Bhanuchander Udhayakumar)

Comprehensive database of standard frequency allocations for wireless
applications. Enables rapid antenna design for specific use cases
without manual frequency lookup.
"""

# Standard frequency allocations for wireless applications
FREQUENCY_BANDS = {
    'GPS_L1': 1.575e9,
    'GPS_L2': 1.227e9,
    'WIFI_2_4GHZ': 2.4e9,
    'WIFI_5GHZ': 5.0e9,
    'BLUETOOTH': 2.45e9,
    'ISM_433MHZ': 433e6,
    'ISM_868MHZ': 868e6,
    'ISM_915MHZ': 915e6,
    'LORA_EU': 868e6,
    'LORA_US': 915e6,
    'CELLULAR_GSM900': 900e6,
    'CELLULAR_GSM1800': 1.8e9,
    'CELLULAR_LTE_B1': 2.1e9,
    'CELLULAR_LTE_B3': 1.8e9,
    'CELLULAR_LTE_B7': 2.6e9,
    'ZIGBEE': 2.4e9,
    'UWB': 6.5e9
}

def get_frequency(band_name):
    """Retrieve frequency for specific band
    
    Case-insensitive lookup for predefined frequency bands.
    Returns frequency in Hz or None if band not found.
    """
    return FREQUENCY_BANDS.get(band_name.upper())

def list_bands():
    """Get list of available frequency bands
    
    Returns list of all bands in the database.
    Use with get_frequency() to access values.
    """
    return list(FREQUENCY_BANDS.keys())

def find_bands_in_range(min_freq, max_freq):
    """Find frequency bands within specified range
    
    Useful for identifying relevant bands for broadband applications
    or regulatory analysis.
    
    Args:
        min_freq: Minimum frequency in Hz
        max_freq: Maximum frequency in Hz
    """
    return {k: v for k, v in FREQUENCY_BANDS.items() if min_freq <= v <= max_freq}

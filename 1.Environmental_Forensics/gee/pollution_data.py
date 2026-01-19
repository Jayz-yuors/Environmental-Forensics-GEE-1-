"""
pollution_data.py
-----------------
Pollution & AQI Forensics – data access layer.
"""

import ee
from gee.data_fetch import fetch_sentinel5p


GAS_BANDS = {
    "NO2": "tropospheric_NO2_column_number_density",
    "SO2": "SO2_column_number_density",
    "CO": "CO_column_number_density",
    "AER_AI": "absorbing_aerosol_index",
}


def get_pollution_composite(region, start_date, end_date, gas="NO2"):
    """
    Compute a median pollution composite for a given gas.
    """
    if gas not in GAS_BANDS:
        raise ValueError(f"Unsupported gas type: {gas}")

    collection = fetch_sentinel5p(region, start_date, end_date, gas)

    composite = (
        collection
        .select(GAS_BANDS[gas])
        .median()
        .clip(region)
        .rename(gas)
    )

    return composite


def get_multi_pollution_stack(region, start_date, end_date):
    """
    Stack multiple pollutants into a single image.
    """
    return (
        get_pollution_composite(region, start_date, end_date, "NO2")
        .addBands(get_pollution_composite(region, start_date, end_date, "SO2"))
        .addBands(get_pollution_composite(region, start_date, end_date, "CO"))
        .addBands(get_pollution_composite(region, start_date, end_date, "AER_AI"))
    )

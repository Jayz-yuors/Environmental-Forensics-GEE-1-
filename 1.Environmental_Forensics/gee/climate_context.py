"""
climate_context.py
------------------
Climate context provider using ERA5-LAND DAILY.

This dataset is stable for small regions and urban analysis.
"""

import ee


def get_climate_composite(region, start_date, end_date):
    """
    Compute mean climate conditions for a time period.
    Uses ERA5-LAND (recommended for land/urban studies).
    """

    collection = (
        ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
        .filterDate(start_date, end_date)
    )

    temperature = (
        collection
        .select("temperature_2m")
        .mean()
        .rename("temperature")
    )

    rainfall = (
        collection
        .select("total_precipitation_sum")
        .mean()
        .rename("rainfall")
    )

    climate = temperature.addBands(rainfall).clip(region)
    return climate

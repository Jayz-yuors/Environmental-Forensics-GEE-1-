"""
pollution_features.py
---------------------
Feature extraction for pollution & AQI proxy analysis.

Transforms Sentinel-5P pollution rasters into numerical features.
"""

import ee


# =========================
# 1. POLLUTION STATISTICS
# =========================

def compute_pollution_statistics(
    pollution_image,
    region,
    scale=1000
):
    """
    Compute basic statistics for a pollution composite.
    """

    stats = pollution_image.reduceRegion(
        reducer=ee.Reducer.mean()
        .combine(ee.Reducer.max(), sharedInputs=True)
        .combine(ee.Reducer.stdDev(), sharedInputs=True),
        geometry=region,
        scale=scale,
        bestEffort=True
    )

    return stats


# =========================
# 2. AQI PROXY SCORE
# =========================

def compute_aqi_proxy(pollution_stack, region):
    """
    Compute a simple AQI proxy score by combining pollutants.
    """

    weights = {
        "NO2": 0.4,
        "SO2": 0.2,
        "CO": 0.2,
        "AER_AI": 0.2,
    }

    weighted_sum = ee.Image(0)

    for band, weight in weights.items():
        weighted_sum = weighted_sum.add(
            pollution_stack.select(band).multiply(weight)
        )

    aqi_proxy = weighted_sum.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=1000,
        bestEffort=True
    )

    return aqi_proxy.get("constant")

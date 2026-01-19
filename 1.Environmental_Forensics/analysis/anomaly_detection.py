"""
anomaly_detection.py
--------------------
Statistical anomaly detection for environmental indicators.
"""

import ee


def zscore_anomaly(image, mean_value, std_value, threshold=2):
    """
    Z-score based anomaly detection.
    """

    mean_img = ee.Image.constant(mean_value)
    std_img = ee.Image.constant(std_value)

    z_score = image.subtract(mean_img).divide(std_img)
    return z_score.abs().gt(threshold).rename("ANOMALY")


def anomaly_score(anomaly_mask, region, scale=30):
    """
    Percentage of region showing anomaly.
    """

    anomalous_pixels = anomaly_mask.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=scale,
        bestEffort=True
    ).values().get(0)

    total_pixels = ee.Image.constant(1).clip(region).reduceRegion(
        reducer=ee.Reducer.count(),
        geometry=region,
        scale=scale,
        bestEffort=True
    ).values().get(0)

    return ee.Number(anomalous_pixels).divide(total_pixels)

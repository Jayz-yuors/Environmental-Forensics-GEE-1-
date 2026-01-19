"""
temporal_features.py
--------------------
Temporal feature engineering for GeoAI.

Focuses on:
- Change stability
- Long-term vs short-term signals
- Variability over time
"""

import ee


# =========================
# 1. TEMPORAL CHANGE STATS
# =========================

def compute_temporal_change_features(
    change_image,
    region,
    scale=10
):
    """
    Extract temporal statistics from a change image (NDVI_CHANGE or similar).
    """

    stats = change_image.reduceRegion(
        reducer=ee.Reducer.mean()
        .combine(ee.Reducer.stdDev(), sharedInputs=True)
        .combine(ee.Reducer.min(), sharedInputs=True)
        .combine(ee.Reducer.max(), sharedInputs=True),
        geometry=region,
        scale=scale,
        bestEffort=True
    )

    return ee.Dictionary({
        "change_mean":stats.get("NDVI_CHANGE_mean"),
        "change_std": stats.get("NDVI_CHANGE_stdDev"),
        "change_min": stats.get("NDVI_CHANGE_min"),
        "change_max": stats.get("NDVI_CHANGE_max"),
    })


# =========================
# 2. PERSISTENCE INDICATOR
# =========================

def compute_persistence_score(change_image, threshold=0.05):
    """
    Estimate persistence of change.
    Lower variability → more persistent change.
    """

    abs_change = change_image.abs()

    persistent_mask = abs_change.gt(threshold)

    persistence_score = persistent_mask.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=change_image.geometry(),
        scale=10,
        bestEffort=True
    )

    return persistence_score.values().get(0)

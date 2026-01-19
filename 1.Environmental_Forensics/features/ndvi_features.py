"""
ndvi_features.py
----------------
Feature engineering for vegetation-based analysis.

Converts NDVI and NDVI_CHANGE images into numerical features
that can be used for severity scoring and ML models.
"""

import ee


# =========================
# 1. BASIC NDVI STATISTICS
# =========================

def compute_ndvi_statistics(ndvi_image, region, scale=10):
    """
    Compute basic NDVI statistics over a region.
    """
    stats = ndvi_image.reduceRegion(
        reducer=ee.Reducer.mean()
        .combine(ee.Reducer.min(), sharedInputs=True)
        .combine(ee.Reducer.max(), sharedInputs=True)
        .combine(ee.Reducer.stdDev(), sharedInputs=True),
        geometry=region,
        scale=scale,
        bestEffort=True
    )

    return stats


# =========================
# 2. NDVI CHANGE STATISTICS
# =========================

def compute_ndvi_change_stats(ndvi_change_image, region, scale=10):
    """
    Compute statistics on NDVI change image.
    """
    stats = ndvi_change_image.reduceRegion(
        reducer=ee.Reducer.mean()
        .combine(ee.Reducer.min(), sharedInputs=True)
        .combine(ee.Reducer.max(), sharedInputs=True),
        geometry=region,
        scale=scale,
        bestEffort=True
    )

    return stats


# =========================
# 3. VEGETATION LOSS AREA %
# =========================

def compute_vegetation_loss_percentage(
    vegetation_loss_mask,
    region,
    scale=10
):
    """
    Compute percentage of area affected by vegetation loss.
    """
    loss_area = vegetation_loss_mask.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=scale,
        bestEffort=True
    )

    total_area = ee.Image.constant(1).clip(region).reduceRegion(
        reducer=ee.Reducer.count(),
        geometry=region,
        scale=scale,
        bestEffort=True
    )

    loss_pixels = ee.Number(loss_area.values().get(0))
    total_pixels = ee.Number(total_area.values().get(0))

    return loss_pixels.divide(total_pixels).multiply(100)


# =========================
# 4. COMBINED FEATURE SET
# =========================

def extract_ndvi_features(
    ndvi_image,
    ndvi_change_image,
    vegetation_loss_mask,
    region
):
    """
    Extract a complete NDVI feature dictionary.
    """
    ndvi_stats = compute_ndvi_statistics(ndvi_image, region)
    change_stats = compute_ndvi_change_stats(ndvi_change_image, region)
    loss_percent = compute_vegetation_loss_percentage(
        vegetation_loss_mask, region
    )

    features = ee.Dictionary({
        "ndvi_mean": ndvi_stats.get("NDVI_mean"),
        "ndvi_min": ndvi_stats.get("NDVI_min"),
        "ndvi_max": ndvi_stats.get("NDVI_max"),
        "ndvi_std": ndvi_stats.get("NDVI_stdDev"),
        "ndvi_change_mean": change_stats.get("NDVI_CHANGE_mean"),
        "ndvi_change_min": change_stats.get("NDVI_CHANGE_min"),
        "ndvi_change_max": change_stats.get("NDVI_CHANGE_max"),
        "vegetation_loss_percent": loss_percent,
    })

    return features

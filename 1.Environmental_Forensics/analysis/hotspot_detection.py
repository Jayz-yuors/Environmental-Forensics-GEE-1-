"""
hotspot_detection.py
--------------------
Detects environmental hotspots based on spatial concentration.
"""

import ee


# =========================
# 1. HOTSPOT DETECTION
# =========================

def detect_hotspots(mask_image, region, threshold=0.6, scale=30):
    """
    Detect spatial hotspots from a binary mask.
    threshold: fraction of neighboring pixels that must be active
    """

    kernel = ee.Kernel.square(radius=1)

    # Neighborhood agreement
    neighborhood = mask_image.convolve(kernel)

    # Normalize by kernel size (9 pixels)
    normalized = neighborhood.divide(9)

    hotspots = normalized.gt(threshold)

    return hotspots.rename("HOTSPOT").clip(region)


# =========================
# 2. HOTSPOT AREA METRIC
# =========================

def hotspot_coverage(hotspot_mask, region, scale=30):
    """
    Percentage of region classified as hotspot.
    """

    hotspot_pixels = hotspot_mask.reduceRegion(
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

    return ee.Number(hotspot_pixels).divide(total_pixels)

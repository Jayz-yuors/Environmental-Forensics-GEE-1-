"""
vegetation_change.py
--------------------
Vegetation Loss Forensics module.

Responsibilities:
- Compute NDVI from Sentinel-2
- Detect NDVI change between two time periods
- Flag abnormal vegetation loss regions

Used by:
- features/ndvi_features.py
- analysis/hotspot_detection.py
- analysis/severity_scoring.py
"""

import ee
from gee.data_fetch import fetch_sentinel2


# =========================
# 1. NDVI COMPUTATION
# =========================

def compute_ndvi(image):
    """
    Compute NDVI for a Sentinel-2 image.
    NDVI = (NIR - RED) / (NIR + RED)
    """
    return image.normalizedDifference(["B8", "B4"]).rename("NDVI")


def get_ndvi_composite(region, start_date, end_date):
    """
    Fetch Sentinel-2 images and compute median NDVI composite.
    """
    collection = fetch_sentinel2(region, start_date, end_date)

    ndvi_collection = collection.map(compute_ndvi)

    return ndvi_collection.median().clip(region)


# =========================
# 2. NDVI CHANGE DETECTION
# =========================

def compute_ndvi_change(region, baseline_period, comparison_period):
    """
    Compute NDVI change between two periods.

    baseline_period: (start_date, end_date)
    comparison_period: (start_date, end_date)
    """
    ndvi_baseline = get_ndvi_composite(
        region, baseline_period[0], baseline_period[1]
    )

    ndvi_comparison = get_ndvi_composite(
        region, comparison_period[0], comparison_period[1]
    )

    ndvi_change = ndvi_comparison.subtract(ndvi_baseline).rename("NDVI_CHANGE")

    return ndvi_change


# =========================
# 3. VEGETATION LOSS FLAGGING
# =========================

def detect_vegetation_loss(
    region,
    baseline_period,
    comparison_period,
    loss_threshold=-0.2
):
    """
    Detect abnormal vegetation loss.

    loss_threshold:
    NDVI change below this value is considered vegetation loss.
    """
    ndvi_change = compute_ndvi_change(
        region, baseline_period, comparison_period
    )

    vegetation_loss_mask = ndvi_change.lt(loss_threshold)

    return vegetation_loss_mask.rename("VEGETATION_LOSS")

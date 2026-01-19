"""
spatial_features.py
-------------------
Spatial feature engineering for GeoAI.

Captures:
- Spatial concentration
- Patchiness / clustering
- Localized vs widespread damage signals
"""

import ee


# =========================
# 1. SPATIAL DENSITY SCORE
# =========================

def compute_spatial_density(mask_image, region, scale=30):
    """
    Measures how spatially concentrated a binary mask is.
    Higher value = more localized (suspicious).
    """

    # Count affected pixels
    affected = mask_image.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=scale,
        bestEffort=True
    ).values().get(0)

    # Total pixels
    total = ee.Image.constant(1).clip(region).reduceRegion(
        reducer=ee.Reducer.count(),
        geometry=region,
        scale=scale,
        bestEffort=True
    ).values().get(0)

    return ee.Number(affected).divide(total)


# =========================
# 2. SPATIAL CLUSTER SCORE
# =========================

def compute_spatial_cluster_score(mask_image):
    """
    Estimates clustering using neighborhood agreement.
    """

    kernel = ee.Kernel.square(radius=1)

    neighborhood_sum = mask_image.convolve(kernel)

    cluster_score = neighborhood_sum.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=mask_image.geometry(),
        scale=30,
        bestEffort=True
    )

    return cluster_score.values().get(0)


# =========================
# 3. COMBINED SPATIAL FEATURES
# =========================

def extract_spatial_features(mask_image, region):
    """
    Extract spatial intelligence features.
    """

    density = compute_spatial_density(mask_image, region)
    clustering = compute_spatial_cluster_score(mask_image)

    return ee.Dictionary({
        "spatial_density": density,
        "spatial_clustering": clustering
    })

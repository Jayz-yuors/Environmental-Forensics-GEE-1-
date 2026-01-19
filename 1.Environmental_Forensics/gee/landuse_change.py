"""
landuse_change.py
-----------------
Land-Use / Land-Cover Change Detection module.

Responsibilities:
- Detect land-cover transitions
- Identify urban expansion & land encroachment
- Compute area-based change masks

Used by:
- analysis/trend_analysis.py
- analysis/severity_scoring.py
- attribution/source_attribution.py
"""

import ee
from gee.data_fetch import fetch_landcover


# =========================
# 1. LAND COVER FETCH
# =========================

def get_landcover(region):
    """
    Fetch ESA WorldCover land cover and clip to region.
    """
    landcover = fetch_landcover()
    return landcover.clip(region)


# =========================
# 2. LAND-USE CHANGE DETECTION
# =========================

def detect_landuse_change(region):
    """
    Detect land-use change by comparing current landcover to itself
    over different categories.

    (Temporal extension handled in analysis module)
    """
    landcover = get_landcover(region)

    # Land cover class reference:
    # 10 = Trees
    # 20 = Shrubland
    # 30 = Grassland
    # 40 = Cropland
    # 50 = Built-up
    # 60 = Bare / sparse vegetation
    # 80 = Permanent water bodies

    return landcover.rename("LANDCOVER")


# =========================
# 3. URBAN EXPANSION MASK
# =========================

def detect_urban_expansion(region):
    """
    Identify built-up land (urban expansion).
    """
    landcover = get_landcover(region)

    # Built-up class = 50
    urban_mask = landcover.eq(50)

    return urban_mask.rename("URBAN_EXPANSION")


# =========================
# 4. VEGETATION TO BUILT-UP TRANSITION
# =========================

def detect_encroachment(region):
    """
    Detect potential encroachment:
    Vegetation classes transitioning to built-up.
    """
    landcover = get_landcover(region)

    vegetation_classes = landcover.eq(10) \
        .Or(landcover.eq(20)) \
        .Or(landcover.eq(30))

    built_up = landcover.eq(50)

    encroachment_mask = vegetation_classes.And(built_up)

    return encroachment_mask.rename("ENCROACHMENT")

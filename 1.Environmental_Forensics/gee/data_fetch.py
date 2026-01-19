"""
data_fetch.py
--------------
Centralized Google Earth Engine data access layer for
Environmental Forensics & Monitoring AI.

This module is responsible ONLY for:
- Initializing Earth Engine
- Fetching raw satellite/climate datasets
- Returning ee.Image or ee.ImageCollection objects

No analysis, no ML, no feature engineering here.
"""

import ee


# =========================
# 1. INITIALIZE GEE
# =========================

def initialize_gee(project_id: str):
    """
    Initialize Google Earth Engine with a specific GCP project.
    """
    try:
        ee.Initialize(project=project_id)
        print("[INFO] Earth Engine initialized successfully.")
    except Exception:
        print("[INFO] Authenticating Earth Engine...")
        ee.Authenticate()
        ee.Initialize(project=project_id)
        print("[INFO] Earth Engine authenticated and initialized.")


# =========================
# 2. REGION HANDLING
# =========================

def get_region_geometry(geometry):
    """
    Accepts an ee.Geometry object and returns it.
    Kept for future validation/extensions.
    """
    if not isinstance(geometry, ee.geometry.Geometry):
        raise ValueError("Input must be an ee.Geometry")
    return geometry


# =========================
# 3. VEGETATION DATA
# =========================
def fetch_sentinel2(region, start_date, end_date):
    """
    Sentinel-2 Harmonized (recommended replacement for deprecated S2).
    """
    return (
        ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
        .filterBounds(region)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
    )
def fetch_landsat(region, start_date, end_date):
    """
    Landsat 8/9 for long-term vegetation & land-use trends.
    """
    return (
        ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
        .filterBounds(region)
        .filterDate(start_date, end_date)
    )


# =========================
# 4. LAND-USE / LAND-COVER
# =========================

def fetch_landcover():
    """
    ESA WorldCover 10m land cover dataset.
    """
    return ee.Image("ESA/WorldCover/v100")


# =========================
# 5. POLLUTION / AIR QUALITY
# =========================

def fetch_sentinel5p(region, start_date, end_date, gas="NO2"):
    """
    Sentinel-5P atmospheric pollutants.

    gas options:
    - "NO2"
    - "SO2"
    - "CO"
    - "AER_AI" (Aerosol Index)
    """
    gas_map = {
        "NO2": "COPERNICUS/S5P/OFFL/L3_NO2",
        "SO2": "COPERNICUS/S5P/OFFL/L3_SO2",
        "CO": "COPERNICUS/S5P/OFFL/L3_CO",
        "AER_AI": "COPERNICUS/S5P/OFFL/L3_AER_AI",
    }

    if gas not in gas_map:
        raise ValueError(f"Unsupported gas type: {gas}")

    return (
        ee.ImageCollection(gas_map[gas])
        .filterBounds(region)
        .filterDate(start_date, end_date)
    )


# =========================
# 6. CLIMATE CONTEXT
# =========================

def fetch_era5(region, start_date, end_date):
    """
    ERA5 climate variables:
    temperature, wind, rainfall
    """
    return (
        ee.ImageCollection("ECMWF/ERA5/DAILY")
        .filterBounds(region)
        .filterDate(start_date, end_date)
    )


# =========================
# 7. ELEVATION
# =========================

def fetch_elevation():
    """
    SRTM Digital Elevation Model (30m).
    """
    return ee.Image("USGS/SRTMGL1_003")


# =========================
# 8. URBAN EXTENT
# =========================

def fetch_urban_extent():
    """
    Global Human Settlement Layer (urban extent).
    """
    return ee.Image("JRC/GHSL/P2023A/GHS_BUILT_S/2020")

from gee.data_fetch import initialize_gee
from gee.vegetation_change import (
    get_ndvi_composite,
    compute_ndvi_change,
    detect_vegetation_loss,
)
from features.ndvi_features import extract_ndvi_features
import ee
import os

initialize_gee("master-sector-469715-h6")

region = ee.Geometry.Point([77.2, 28.6]).buffer(20000)

ndvi = get_ndvi_composite(region, "2019-01-01", "2019-12-31")
ndvi_change = compute_ndvi_change(
    region,
    ("2019-01-01", "2019-12-31"),
    ("2023-01-01", "2023-12-31"),
)
veg_loss = detect_vegetation_loss(
    region,
    ("2019-01-01", "2019-12-31"),
    ("2023-01-01", "2023-12-31"),
)

features = extract_ndvi_features(
    ndvi, ndvi_change, veg_loss, region
)

print(features.getInfo())

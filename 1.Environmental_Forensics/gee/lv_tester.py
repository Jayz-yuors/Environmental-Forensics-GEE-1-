from data_fetch import initialize_gee
from vegetation_change import detect_vegetation_loss
import ee
import os

initialize_gee("master-sector-469715-h6")

region = ee.Geometry.Point([77.2, 28.6]).buffer(20000)

mask = detect_vegetation_loss(
    region,
    baseline_period=("2019-01-01", "2019-12-31"),
    comparison_period=("2023-01-01", "2023-12-31")
)

print(mask.bandNames().getInfo())

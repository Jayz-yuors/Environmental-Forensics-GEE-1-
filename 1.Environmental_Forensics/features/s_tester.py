from gee.data_fetch import initialize_gee
from gee.vegetation_change import detect_vegetation_loss
from features.spatial_features import extract_spatial_features
import ee


initialize_gee("master-sector-469715-h6")

region = ee.Geometry.Point([77.2, 28.6]).buffer(20000)

baseline = ("2019-01-01", "2019-12-31")
comparison = ("2023-01-01", "2023-12-31")

veg_loss = detect_vegetation_loss(
    region, baseline, comparison
)

spatial_features = extract_spatial_features(
    veg_loss, region
)

print("Spatial features:", spatial_features.getInfo())

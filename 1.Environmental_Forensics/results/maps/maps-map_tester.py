from gee.data_fetch import initialize_gee
from results.maps.severity_map import generate_severity_map
import ee


initialize_gee("master-sector-469715-h6")

region = ee.Geometry.Point([77.2, 28.6]).buffer(20000)


# Mock values (from pipeline)
vegetation_loss_pct = ee.Number(0.42)
anomaly_pct = ee.Number(0.13)
hotspot_pct = ee.Number(0.02)
aqi_proxy = ee.Number(0.06)


severity_map = generate_severity_map(
    vegetation_loss_pct,
    anomaly_pct,
    hotspot_pct,
    aqi_proxy,
    region
)

print("Severity map band names:", severity_map.bandNames().getInfo())

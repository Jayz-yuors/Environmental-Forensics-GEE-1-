from gee.data_fetch import initialize_gee
from gee.vegetation_change import (
    get_ndvi_composite,
    detect_vegetation_loss
)
from analysis.hotspot_detection import detect_hotspots, hotspot_coverage
from analysis.anomaly_detection import zscore_anomaly, anomaly_score
import ee


initialize_gee("master-sector-469715-h6")

region = ee.Geometry.Point([77.2, 28.6]).buffer(20000)

baseline = ("2019-01-01", "2019-12-31")
comparison = ("2023-01-01", "2023-12-31")


veg_loss = detect_vegetation_loss(region, baseline, comparison)

hotspots = detect_hotspots(veg_loss, region)
hotspot_pct = hotspot_coverage(hotspots, region)

ndvi_base = get_ndvi_composite(region, baseline[0], baseline[1])
ndvi_comp = get_ndvi_composite(region, comparison[0], comparison[1])

stats = ndvi_base.reduceRegion(
    reducer=ee.Reducer.mean().combine(
        ee.Reducer.stdDev(),
        sharedInputs=True
    ),
    geometry=region,
    scale=30,
    bestEffort=True
)

mean = stats.get("NDVI_mean")
std = stats.get("NDVI_stdDev")

anomaly_mask = zscore_anomaly(ndvi_comp, mean, std)
anomaly_pct = anomaly_score(anomaly_mask, region)

print("Hotspot coverage:", hotspot_pct.getInfo())
print("Anomaly coverage:", anomaly_pct.getInfo())

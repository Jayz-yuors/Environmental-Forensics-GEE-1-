from gee.data_fetch import initialize_gee
from gee.vegetation_change import (
    compute_ndvi_change,
    detect_vegetation_loss,
)
from gee.pollution_data import get_multi_pollution_stack
from features.temporal_features import (
    compute_temporal_change_features,
    compute_persistence_score,
)
from features.pollution_features import (
    compute_pollution_statistics,
    compute_aqi_proxy,
)
import ee


# =========================
# INIT
# =========================

initialize_gee("master-sector-469715-h6")

region = ee.Geometry.Point([77.2, 28.6]).buffer(20000)

baseline = ("2019-01-01", "2019-12-31")
comparison = ("2023-01-01", "2023-12-31")


# =========================
# TEMPORAL FEATURES TEST
# =========================

ndvi_change = compute_ndvi_change(region, baseline, comparison)

temporal_features = compute_temporal_change_features(
    ndvi_change, region
)

persistence = compute_persistence_score(ndvi_change)

print("Temporal features:", temporal_features.getInfo())
print("Persistence score:", persistence.getInfo())


# =========================
# POLLUTION FEATURES TEST
# =========================

pollution = get_multi_pollution_stack(
    region,
    "2023-01-01",
    "2023-12-31"
)

pollution_stats = compute_pollution_statistics(
    pollution, region
)

aqi_score = compute_aqi_proxy(pollution, region)

print("Pollution stats:", pollution_stats.getInfo())
print("AQI proxy score:", aqi_score.getInfo())

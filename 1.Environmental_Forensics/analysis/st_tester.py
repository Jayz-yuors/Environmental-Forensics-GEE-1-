from gee.data_fetch import initialize_gee
from analysis.severity_scoring import compute_severity_score
from analysis.trend_analysis import compute_ndvi_trend, trend_severity
import ee


initialize_gee("master-sector-469715-h6")

region = ee.Geometry.Point([77.2, 28.6]).buffer(20000)


vegetation_loss_pct = ee.Number(0.42)
anomaly_pct = ee.Number(0.04)
hotspot_pct = ee.Number(0.01)
aqi_proxy = ee.Number(0.03)

severity = compute_severity_score(
    vegetation_loss_pct,
    anomaly_pct,
    hotspot_pct,
    aqi_proxy
)

print("Severity score:", severity.getInfo())


trend_img = compute_ndvi_trend(region, 2018, 2023)
trend_score = trend_severity(trend_img, region)

print("Trend degradation score:", trend_score.getInfo())

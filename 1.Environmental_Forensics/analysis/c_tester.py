from gee.data_fetch import initialize_gee
from analysis.city_comparison import build_city_severity_fc, rank_cities
import ee


initialize_gee("master-sector-469715-h6")


cities = {
    "Delhi": {
        "vegetation_loss": ee.Number(0.42),
        "anomaly": ee.Number(0.13),
        "hotspot": ee.Number(0.02),
        "aqi": ee.Number(0.06),
    },
    "Mumbai": {
        "vegetation_loss": ee.Number(0.25),
        "anomaly": ee.Number(0.08),
        "hotspot": ee.Number(0.01),
        "aqi": ee.Number(0.04),
    },
    "Bangalore": {
        "vegetation_loss": ee.Number(0.18),
        "anomaly": ee.Number(0.05),
        "hotspot": ee.Number(0.0),
        "aqi": ee.Number(0.02),
    },
}


city_fc = build_city_severity_fc(cities)
ranking_fc = rank_cities(city_fc)

print("City ranking (worst → best):")
print(ranking_fc.getInfo())

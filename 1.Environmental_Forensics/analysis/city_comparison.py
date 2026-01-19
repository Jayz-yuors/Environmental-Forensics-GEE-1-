"""
city_comparison.py
------------------
Cross-city and cross-region comparative analysis.
Earth Engine SAFE implementation.
"""

import ee
from analysis.severity_scoring import compute_severity_score


# =========================
# BUILD CITY SEVERITY TABLE
# =========================

def build_city_severity_fc(city_feature_dict):
    """
    Convert city metrics into a FeatureCollection.
    """

    features = []

    for city, f in city_feature_dict.items():
        severity = compute_severity_score(
            f["vegetation_loss"],
            f["anomaly"],
            f["hotspot"],
            f["aqi"]
        )

        feat = ee.Feature(
            None,
            {
                "city": city,
                "severity": severity
            }
        )

        features.append(feat)

    return ee.FeatureCollection(features)


# =========================
# RANKING (EE NATIVE)
# =========================

def rank_cities(city_fc):
    """
    Rank cities by severity (descending).
    """

    return city_fc.sort("severity", False)

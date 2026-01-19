"""
severity_map.py
---------------
Generate map-ready layers for environmental severity visualization.
"""

import ee
from analysis.severity_scoring import compute_severity_score


# =========================
# SEVERITY MAP
# =========================

def generate_severity_map(
    vegetation_loss_pct,
    anomaly_pct,
    hotspot_pct,
    aqi_proxy,
    region
):
    """
    Create a constant-image severity map for visualization.
    """

    severity_score = compute_severity_score(
        vegetation_loss_pct,
        anomaly_pct,
        hotspot_pct,
        aqi_proxy
    )

    severity_img = ee.Image.constant(severity_score).clip(region)

    return severity_img.rename("SEVERITY")

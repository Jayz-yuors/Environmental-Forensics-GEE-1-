"""
severity_scoring.py
-------------------
Compute unified environmental severity score (0–100).

Inputs:
- Vegetation loss %
- Anomaly %
- Hotspot %
- Pollution AQI proxy

Output:
- Single interpretable severity score
"""

import ee


# =========================
# NORMALIZATION UTILS
# =========================

def clamp(value, min_val=0, max_val=1):
    return ee.Number(value).max(min_val).min(max_val)


def normalize(value, max_expected):
    return clamp(ee.Number(value).divide(max_expected))


# =========================
# SEVERITY SCORE
# =========================

def compute_severity_score(
    vegetation_loss_pct,
    anomaly_pct,
    hotspot_pct,
    aqi_proxy,
):
    """
    Returns severity score (0–100)
    """

    # Normalize inputs
    veg_score = normalize(vegetation_loss_pct, 0.6)
    anomaly_score = normalize(anomaly_pct, 0.3)
    hotspot_score = normalize(hotspot_pct, 0.3)
    pollution_score = normalize(aqi_proxy, 0.1)

    # Weighted fusion
    severity = (
        veg_score.multiply(0.35)
        .add(anomaly_score.multiply(0.25))
        .add(hotspot_score.multiply(0.2))
        .add(pollution_score.multiply(0.2))
    )

    return severity.multiply(100)

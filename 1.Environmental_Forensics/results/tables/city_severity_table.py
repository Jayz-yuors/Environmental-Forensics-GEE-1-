"""
city_severity_table.py
----------------------
Generate ranked city severity tables from analysis outputs.

Output:
- Python list of dicts
- Optional CSV export
"""

import ee
import csv
from analysis.city_comparison import build_city_severity_fc, rank_cities


# =========================
# TABLE GENERATION
# =========================

def generate_city_severity_table(city_feature_dict):
    """
    Returns a ranked list of city severity records.
    """

    city_fc = build_city_severity_fc(city_feature_dict)
    ranked_fc = rank_cities(city_fc)

    features = ranked_fc.getInfo()["features"]

    table = []

    for rank, f in enumerate(features, start=1):
        props = f["properties"]
        table.append({
            "rank": rank,
            "city": props["city"],
            "severity_score": round(props["severity"], 2)
        })

    return table


# =========================
# CSV EXPORT (OPTIONAL)
# =========================

def export_table_to_csv(table, filepath):
    """
    Export severity table to CSV.
    """

    if not table:
        raise ValueError("Empty table cannot be exported")

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=table[0].keys())
        writer.writeheader()
        writer.writerows(table)

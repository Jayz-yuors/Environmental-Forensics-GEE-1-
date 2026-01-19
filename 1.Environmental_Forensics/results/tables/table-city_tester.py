from gee.data_fetch import initialize_gee
from results.tables.city_severity_table import (
    generate_city_severity_table,
    export_table_to_csv
)
import ee
import os


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


table = generate_city_severity_table(cities)

print("City Severity Table:")
for row in table:
    print(row)


# Optional CSV export
output_path = "results/tables/city_severity.csv"
export_table_to_csv(table, output_path)

print(f"\nCSV exported to: {output_path}")

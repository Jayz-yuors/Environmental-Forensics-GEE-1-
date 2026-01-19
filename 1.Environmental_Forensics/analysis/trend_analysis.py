"""
trend_analysis.py
-----------------
Long-term environmental trend analysis.
"""

import ee
from gee.vegetation_change import get_ndvi_composite


def compute_ndvi_trend(region, year_start, year_end):
    """
    Compute NDVI trend slope using year as independent variable.
    """

    def yearly_ndvi(year):
        year = ee.Number(year).toFloat()

        start = ee.Date.fromYMD(year, 1, 1)
        end = ee.Date.fromYMD(year, 12, 31)

        ndvi = get_ndvi_composite(
            region,
            start.format("YYYY-MM-dd"),
            end.format("YYYY-MM-dd"),
        ).rename("NDVI")

        # IMPORTANT: cast year to Float image
        year_band = ee.Image.constant(year).toFloat().rename("year")

        return ndvi.addBands(year_band)

    years = ee.List.sequence(year_start, year_end)
    collection = ee.ImageCollection(years.map(yearly_ndvi))

    trend = collection.select(["year", "NDVI"]).reduce(
        ee.Reducer.linearFit()
    )

    return trend.select("scale").rename("NDVI_TREND")


def trend_severity(trend_image, region):
    """
    Convert NDVI trend to degradation score.
    """

    mean_trend = trend_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=30,
        bestEffort=True
    ).values().get(0)

    # Negative trend → degradation
    return ee.Number(mean_trend).multiply(-1).max(0)

import ee
ee.Initialize(project='master-sector-469715-h6')

roi = ee.Geometry.Rectangle([72, 18, 74, 20])  # Maharashtra sample

image = ee.Image('USGS/SRTMGL1_003')

stats = image.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=roi,
    scale=30,
    maxPixels=1e9
)

print(stats.getInfo())

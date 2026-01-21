import ee
import geemap
import os

# 1. INITIALIZATION
try:
    ee.Initialize(project='master-sector-469715-h6')
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project='master-sector-469715-h6')

# 2. DEFINE AREA (Using the same Delhi coordinates)
poi = ee.Geometry.Point([77.2090, 28.6139]) 
region = poi.buffer(3000).bounds()

# 3. SATELLITE IMAGERY
image = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
         .filterBounds(region)
         .filterDate('2023-01-01', '2023-12-31')
         .sort('CLOUDY_PIXEL_PERCENTAGE')
         .first()
         .clip(region))

# 4. ALGORITHMS (The Markings)
ndvi = image.normalizedDifference(['B8', 'B4'])
green_mask = ndvi.updateMask(ndvi.gt(0.3)).visualize(palette=['#00FF00'], opacity=0.6)

ndbi = image.normalizedDifference(['B11', 'B8'])
red_mask = ndbi.updateMask(ndbi.gt(0.1)).visualize(palette=['#FF0000'], opacity=0.6)

# Base Map (Natural Color RGB)
rgb_base = image.visualize(bands=['B4', 'B3', 'B2'], min=0, max=3500)

# Merge for Heatmap
final_heatmap = rgb_base.blend(green_mask).blend(red_mask)

# 5. DOWNLOAD BOTH FILES
files = {
    "1_original_satellite.png": rgb_base,
    "2_marked_heatmap.png": final_heatmap
}

for name, img_obj in files.items():
    out_path = os.path.join(os.getcwd(), name)
    print(f"Downloading {name}...")
    try:
        geemap.get_image_thumbnail(
            img_obj, 
            out_path, 
            vis_params={}, 
            dimensions=1024, 
            format='png', 
            region=region
        )
    except Exception as e:
        print(f"Failed to download {name}: {e}")

print("\nFinished! You now have both the raw satellite view and your heatmap in the folder.")
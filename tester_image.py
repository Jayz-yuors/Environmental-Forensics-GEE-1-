import ee
import geemap
import webbrowser
import os

try:
    # 1. INITIALIZATION
    # Linking to your specific project ID
    ee.Initialize(project='master-sector-469715-h6')
    print("Successfully connected to Earth Engine Project: master-sector-469715-h6")

    # 2. SATELLITE IMAGERY (Data Input)
    # Using a sample location (New York City)
    region = ee.Geometry.Point([-74.006, 40.7128])
    image = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
             .filterBounds(region)
             .filterDate('2023-01-01', '2023-12-31')
             .sort('CLOUDY_PIXEL_PERCENTAGE')
             .first())

    # 3. YOUR ALGORITHM (Processing)
    # Simple algorithm to mask clouds based on the QA band
    qa = image.select('MSK_CLDPRB')
    cloud_free = image.updateMask(qa.lt(20))

    # 4. REAL WORLD APPLICATION (Output)
    # Since you are in a terminal, we save the map to a file
    Map = geemap.Map()
    Map.centerObject(region, 12)
    Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'max': 3000}, 'Original Satellite')
    Map.addLayer(cloud_free, {'bands': ['B4', 'B3', 'B2'], 'max': 3000}, 'Cloud Filtered Algorithm')

    # Save and Open
    output_file = 'ee_test_result.html'
    Map.save(output_file)
    
    print(f"Test Successful! Opening {output_file} in your browser...")
    webbrowser.open('file://' + os.path.realpath(output_file))

except Exception as e:
    print(f"An error occurred: {e}")
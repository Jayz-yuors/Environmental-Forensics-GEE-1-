from data_fetch import initialize_gee
from pollution_data import get_multi_pollution_stack
from climate_context import get_climate_composite
import ee


initialize_gee("master-sector-469715-h6")

region = ee.Geometry.Point([77.2, 28.6]).buffer(20000)
start_date = "2023-01-01"
end_date = "2023-12-31"

pollution = get_multi_pollution_stack(region, start_date, end_date)
print("Pollution bands:", pollution.bandNames().getInfo())

climate = get_climate_composite(region, start_date, end_date)

# Force evaluation
print("Climate bands:", ee.Image(climate).bandNames().getInfo())


from data_fetch import initialize_gee, fetch_elevation
import os

# Read project ID from environment variable

# IMPORTANT: pass the variable, NOT a string
initialize_gee("master-sector-469715-h6")

elev = fetch_elevation()
print(elev.getInfo()["id"])

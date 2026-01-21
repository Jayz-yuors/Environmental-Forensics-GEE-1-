CREATE TABLE spatial_assets (
    asset_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(city_id),
    year INT,
    month INT,
    asset_type TEXT,
    storage_path TEXT,
    resolution TEXT,
    source TEXT
);

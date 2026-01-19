CREATE TABLE ml_features (
    feature_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(city_id),
    time_id INT REFERENCES time_dim(time_id),

    ndvi_change FLOAT,
    pollution_trend FLOAT,
    anomaly_score FLOAT,
    hotspot_density FLOAT,
    persistence_score FLOAT
);

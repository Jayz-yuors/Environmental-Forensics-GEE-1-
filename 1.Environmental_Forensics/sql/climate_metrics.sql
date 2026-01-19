CREATE TABLE climate_metrics (
    climate_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(city_id),
    time_id INT REFERENCES time_dim(time_id),

    temperature_mean FLOAT,
    rainfall_total FLOAT,
    wind_speed_mean FLOAT
);

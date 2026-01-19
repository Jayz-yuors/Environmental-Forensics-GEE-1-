CREATE TABLE pollution_metrics (
    poll_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(city_id),
    time_id INT REFERENCES time_dim(time_id),

    no2_mean FLOAT,
    so2_mean FLOAT,
    co_mean FLOAT,
    aerosol_index FLOAT,

    aqi_proxy FLOAT,
    geom GEOMETRY(Polygon, 4326)
);

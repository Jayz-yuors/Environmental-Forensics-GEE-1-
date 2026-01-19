CREATE TABLE vegetation_metrics (
    veg_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(city_id),
    time_id INT REFERENCES time_dim(time_id),

    ndvi_mean FLOAT,
    ndvi_min FLOAT,
    ndvi_max FLOAT,
    ndvi_std FLOAT,

    vegetation_loss_pct FLOAT,
    geom GEOMETRY(Polygon, 4326)
);

CREATE TABLE trend_metrics (
    trend_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(city_id),

    start_year INT,
    end_year INT,
    ndvi_trend_slope FLOAT,
    pollution_trend_slope FLOAT,
    degradation_score FLOAT
);

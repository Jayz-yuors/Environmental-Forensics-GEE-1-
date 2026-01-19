CREATE TABLE severity_scores (
    severity_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(city_id),
    time_id INT REFERENCES time_dim(time_id),

    vegetation_weight FLOAT,
    pollution_weight FLOAT,
    anomaly_weight FLOAT,

    final_severity_score FLOAT CHECK (final_severity_score BETWEEN 0 AND 100),
    risk_level TEXT
);

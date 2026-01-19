CREATE TABLE city_rankings (
    ranking_id SERIAL PRIMARY KEY,
    time_id INT REFERENCES time_dim(time_id),

    city_id INT REFERENCES cities(city_id),
    severity_score FLOAT,
    rank INT
);

CREATE TABLE time_dim (
    time_id SERIAL PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    quarter INT,
    start_date DATE,
    end_date DATE,
    UNIQUE (year, month)
);

CREATE TABLE data_exports (
    export_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(city_id),
    time_id INT REFERENCES time_dim(time_id),

    export_type TEXT,   -- map / table / chart / report
    file_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

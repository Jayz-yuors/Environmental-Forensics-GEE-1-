CREATE TABLE data_ingestion_log (
    ingestion_id SERIAL PRIMARY KEY,
    source TEXT,
    dataset TEXT,
    city_id INT REFERENCES cities(city_id),
    start_date DATE,
    end_date DATE,
    status TEXT,
    records_fetched INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE model_registry (
    model_id SERIAL PRIMARY KEY,
    model_name TEXT,
    version TEXT,
    trained_on_from DATE,
    trained_on_to DATE,
    metrics JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

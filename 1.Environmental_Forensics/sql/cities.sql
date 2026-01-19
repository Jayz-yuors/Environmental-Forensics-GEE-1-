CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name TEXT UNIQUE NOT NULL,
    country TEXT DEFAULT 'India',
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geom GEOMETRY(Point, 4326)
);

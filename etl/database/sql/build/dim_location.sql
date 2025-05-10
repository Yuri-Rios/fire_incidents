CREATE TABLE IF NOT EXISTS dim_location (
    location_id SERIAL PRIMARY KEY,
    address TEXT,
    city TEXT,
    zipcode TEXT,
    neighborhood TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

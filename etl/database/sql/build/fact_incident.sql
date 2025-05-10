CREATE TABLE IF NOT EXISTS fact_incident (
    incident_id BIGINT PRIMARY KEY,
    date_id INT REFERENCES dim_date(date_id),
    location_id INT REFERENCES dim_location(location_id),
    call_type TEXT,
    number_of_units INT,
    priority TEXT,
    response_delay DOUBLE PRECISION,
    available_date TIMESTAMP
);

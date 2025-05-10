CREATE TABLE IF NOT EXISTS dim_date (
        date_id SERIAL PRIMARY KEY,
        full_date DATE NOT NULL,
        day INT,
        month INT,
        year INT,
        weekday VARCHAR(10)
        );

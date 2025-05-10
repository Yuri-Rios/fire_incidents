CREATE USER admin WITH PASSWORD 'admin';

CREATE DATABASE fire_incidents;

GRANT ALL PRIVILEGES ON DATABASE fire_incidents TO admin;

ALTER SCHEMA public OWNER TO admin;

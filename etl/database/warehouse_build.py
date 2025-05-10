"""
Pipeline first run. Create tables.
"""

import os
from pathlib import Path
import psycopg

# Default dir for SQL files
BASE_DIR = Path(__file__).resolve().parent / "sql/build"

def execute_sql_file(cur, filepath):
    try:
        with open(filepath, "r") as file:
            sql = file.read()
            cur.execute(sql)
            print(f"Executado com sucesso: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"Erro ao executar {filepath}: {e}")
        raise

# PostgreSQL connection
try:
    conn = psycopg.connect(
        "host=localhost dbname=fire_incidents user=admin password=admin"
    )
except Exception as e:
    raise RuntimeError(f"Postgres comunication error: {e}")

# Run SQL files
with conn:
    with conn.cursor() as cur:
        sql_files = [
            BASE_DIR/"dim_date.sql",
            BASE_DIR/"dim_location.sql",
            BASE_DIR/"fact_incident.sql",
            BASE_DIR/"fire_incident_temp.sql"

        ]
        for sql_file in sql_files:
            execute_sql_file(cur, sql_file)

print("Todas as tabelas foram criadas com sucesso!")

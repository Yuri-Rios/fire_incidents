"""
Create functions to be used in data warehouse and medallion pipeline.
"""

import os
import re
from datetime import datetime, timedelta
import psycopg2

def get_recent_json_files(directory: str, lookback_days: int) -> list:
    """
    Returns a list of absolute paths to .jsonl files in the given directory
    that match a date-based pattern and fall within the given number of lookback days.

    The function looks for a date pattern (YYYYMMDD) followed by 'T' in the filename.

    Parameters:
    ----------
    directory : str
        Path to the directory containing the .jsonl files.
    lookback_days : int
        How many days back from today to include files.

    Returns:
    -------
    list
        A list of full paths to files that match the criteria.
    """
    cutoff_date = datetime.today() - timedelta(days=lookback_days)
    file_list = []

    for fname in os.listdir(directory):
        # Look for a date pattern like 20250510T in the filename
        match = re.search(r"(\d{8})T", fname)
        if match:
            file_date = datetime.strptime(match.group(1), "%Y%m%d")
            if file_date >= cutoff_date and fname.endswith(".jsonl"):
                file_list.append(os.path.join(directory, fname))

    return file_list

def upsert_fire_incident_temp(
        df,
        jdbc_url,
        db_properties,
        primary_key="incident_number",
        update_columns=None):
    """
    Writes the given Spark DataFrame to a staging PostgreSQL table
    and performs an upsert into the same table.

    :param df: Spark DataFrame
    :param jdbc_url: JDBC URL for PostgreSQL
    :param db_properties: JDBC properties (user, password, driver)
    :param primary_key: Primary key column
    :param update_columns: Columns to update; if None or empty,
                           all columns except the PK are updated
    """

    # Step 1: Write temp data into fire_incident_temp (overwriting)
    df.write \
        .mode("overwrite") \
        .jdbc(url=jdbc_url, table="fire_incident_temp", properties=db_properties)

    # Step 2: Generate SQL for upsert
    columns = df.columns
    if update_columns is None or not update_columns:
        update_columns = [col for col in columns if col != primary_key]

    update_stmt = ", ".join([f"{col}=EXCLUDED.{col}" for col in update_columns])
    insert_columns = ", ".join(columns)

    sql = f"""
    INSERT INTO fire_incident_temp ({insert_columns})
    SELECT {insert_columns} FROM fire_incident_temp_staging
    ON CONFLICT ({primary_key}) DO UPDATE
    SET {update_stmt};
    """

    # Step 3: Run the merge in PostgreSQL
    conn = psycopg2.connect(
        dbname="fire_incidents",
        user=db_properties["user"],
        password=db_properties["password"],
        host="localhost",
        port=5432
    )
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

    print("Upsert executed successfully.")

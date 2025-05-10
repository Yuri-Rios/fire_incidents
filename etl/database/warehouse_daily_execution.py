"""
Main pipeline execution
"""
# Add root folder to sys.path before importing local modules
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import others lib
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from datetime import datetime
from helpers.python_utils import get_recent_json_files, upsert_fire_incident_temp


SPARK_JAR_PATH = "/workspaces/fire_incidents/jars/postgresql-42.7.3.jar"
DATA_SOURCE = "/workspaces/fire_incidents/storage/ingestion/"
LOOK_BACK_DAYS = 3
JBC_UR = "jdbc:postgresql://localhost:5432/fire_incidents"

# Spark Init
spark = SparkSession.builder \
    .appName("FireIncidentsDW") \
    .config("spark.jars", SPARK_JAR_PATH) \
    .getOrCreate()

# List Json Files
files_to_read = get_recent_json_files(DATA_SOURCE, LOOK_BACK_DAYS)
# Read and transform
df = spark.read.option("multiLine", False).json(files_to_read)
# Transform
df = df.withColumn("longitude", col("point.coordinates")[0]) \
       .withColumn("latitude", col("point.coordinates")[1]) \
       .drop("point") \
       .withColumn("metadata_ingestion_batch_id",lit(f"{datetime.now().strftime('%Y%m%dT%H%M%S')}"))


# Writes in Postgres

db_properties = {
    "user": "admin",
    "password": "admin",
    "driver": "org.postgresql.Driver"
}

upsert_fire_incident_temp(df, JBC_UR, db_properties)

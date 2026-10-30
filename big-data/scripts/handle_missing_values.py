from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create Spark Session
spark = SparkSession.builder \
    .appName("HandleMissingValues") \
    .master("local[*]") \
    .getOrCreate()

# Locate CSV file
project_folder = Path(__file__).resolve().parent.parent
csv_file = project_folder / "data" / "all_complaints.csv"

# Load dataset
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("nullValue", "NULL") \
    .csv(str(csv_file))

# Count missing locations before filling
missing_location = df.filter(
    col("location").isNull()
).count()

print("Missing locations before filling:", missing_location)

# Replace missing locations
cleaned_df = df.fillna({"location": "Unknown"})

# Count missing locations after filling
missing_after = cleaned_df.filter(
    col("location").isNull()
).count()

print("Missing locations after filling:", missing_after)

# Display records
cleaned_df.select(
    "id", "name", "location"
).show(10)

# Stop Spark
spark.stop()
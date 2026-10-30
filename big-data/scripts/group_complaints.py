from pathlib import Path
from pyspark.sql import SparkSession


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

# Group complaints by category
category_count = df.groupBy("category").count()

# Display results
print("Total Complaints by Category:")

category_count.show()

# Stop Spark
spark.stop()
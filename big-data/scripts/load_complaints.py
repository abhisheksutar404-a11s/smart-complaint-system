
from pathlib import Path
from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("SmartComplaintDataLoading") \
    .master("local[*]") \
    .getOrCreate()

# Locate the combined CSV file
project_folder = Path(__file__).resolve().parent.parent
csv_file = project_folder / "data" / "all_complaints.csv"

# Load CSV into Spark DataFrame
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("nullValue", "NULL") \
    .csv(str(csv_file))

# Display results
print("Dataset loaded successfully!")

print("\nFirst 5 complaints:")
df.show(5, truncate=False)

print("\nDataset Schema:")
df.printSchema()

print("\nTotal number of complaints:")
print(df.count())

# Stop Spark
spark.stop()


from pathlib import Path
from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("ComplaintFiltering") \
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

# Filter High Priority Complaints
high_priority_df = df.filter(df.priority == "High")

# Display results
print("High Priority Complaints:")
high_priority_df.show(10)

# Count High Priority Complaints
print("Total High Priority Complaints:", high_priority_df.count())

# Stop Spark
spark.stop()
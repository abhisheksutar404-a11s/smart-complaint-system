from pathlib import Path
from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("ComplaintColumnSelection") \
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

# Select specific columns
selected_df = df.select(
    "id",
    "category",
    "priority",
    "status"
)

# Display selected columns
print("Selected Complaint Columns:")
selected_df.show(10)

# Stop Spark
spark.stop()
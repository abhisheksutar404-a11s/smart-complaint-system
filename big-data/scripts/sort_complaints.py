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

# Sort categories by complaint count (highest to lowest)
sorted_categories = category_count.orderBy(
    category_count["count"].desc()
)

# Display sorted results
print("Complaints by Category (Highest to Lowest):")
sorted_categories.show()

# Stop Spark
spark.stop()
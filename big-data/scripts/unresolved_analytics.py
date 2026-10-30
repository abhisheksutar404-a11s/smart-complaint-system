
from pathlib import Path
from pyspark.sql import SparkSession

# 1. Create Spark Session
spark = SparkSession.builder \
    .appName("UnresolvedComplaintAnalytics") \
    .master("local[*]") \
    .getOrCreate()

# 2. Locate CSV file
project_folder = Path(__file__).resolve().parent.parent
csv_file = project_folder / "data" / "all_complaints.csv"

# 3. Load complaint dataset
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("nullValue", "NULL") \
    .csv(str(csv_file))

# 4. Filter unresolved complaints
unresolved_df = df.filter(
    df.status.isin("Open", "Pending", "In Progress")
)

# 5. Count unresolved complaints
unresolved_count = unresolved_df.count()

# 6. Count resolved complaints
resolved_count = df.filter(
    df.status == "Resolved"
).count()

# 7. Display results
print("UNRESOLVED COMPLAINT ANALYTICS")
print("Total Unresolved Complaints:", unresolved_count)
print("Total Resolved Complaints:", resolved_count)

# 8. Stop Spark
spark.stop()

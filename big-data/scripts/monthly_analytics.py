
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import year, month

# 1. Create Spark Session
spark = SparkSession.builder \
    .appName("MonthlyComplaintAnalytics") \
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

# 4. Extract year and month
monthly_df = df.withColumn(
    "year", year("created_at")
).withColumn(
    "month", month("created_at")
)

# 5. Group complaints by year and month
monthly_count = monthly_df.groupBy(
    "year", "month"
).count()

# 6. Sort by year and month
monthly_analytics = monthly_count.orderBy(
    "year", "month"
)

# 7. Display results
print("MONTHLY COMPLAINT ANALYTICS")
monthly_analytics.show()

# 8. Stop Spark
spark.stop()

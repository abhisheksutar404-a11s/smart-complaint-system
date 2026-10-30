
from pathlib import Path
from pyspark.sql import SparkSession

# 1. Create Spark Session
spark = SparkSession.builder \
    .appName("PriorityAnalytics") \
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

# 4. Calculate priority-wise complaints
priority_count = df.groupBy("priority").count()

# 5. Sort by priority
priority_analytics = priority_count.orderBy(
    "priority"
)

# 6. Display analytics
print("PRIORITY-WISE COMPLAINT ANALYTICS")
priority_analytics.show()

# 7. Stop Spark
spark.stop()

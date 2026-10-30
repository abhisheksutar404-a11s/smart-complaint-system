import csv

from pathlib import Path
from pyspark.sql import SparkSession

# 1. Create Spark Session
spark = SparkSession.builder \
    .appName("CategoryAnalytics") \
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

# 4. Calculate category-wise complaints
category_count = df.groupBy("category").count()

# 5. Sort from highest to lowest
category_analytics = category_count.orderBy(
    "count", ascending=False
)

# 6. Display analytics
print("CATEGORY-WISE COMPLAINT ANALYTICS")
category_analytics.show()

# 7. Export analytics to CSV
output_file = project_folder / "output" / "mysql_category_analytics" / "category_analytics.csv"

output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["category", "count"])

    for row in category_analytics.collect():
        writer.writerow([row["category"], row["count"]])

print("Analytics CSV exported successfully!")
print("Output file:", output_file)

# 8. Stop Spark
spark.stop()


import os
import csv
from pathlib import Path
from pyspark.sql import SparkSession

# 1. Locate MySQL JDBC Driver
project_folder = Path(__file__).resolve().parent.parent
jar_file = project_folder / "jars" / "mysql-connector-j-26.10.0.jar"

# 2. Read MySQL credentials
mysql_user = os.getenv("DB_USERNAME")
mysql_password = os.getenv("DB_PASSWORD")

if not mysql_user or not mysql_password:
    raise ValueError("Please configure MYSQL_USER and MYSQL_PASSWORD.")

# 3. Create Spark Session
spark = SparkSession.builder \
    .appName("SmartComplaintMySQLAnalytics") \
    .master("local[*]") \
    .config("spark.driver.extraClassPath", str(jar_file)) \
    .getOrCreate()

# 4. MySQL Database URL
jdbc_url = "jdbc:mysql://localhost:3306/smart_complaint_db"

# 5. Read complaint table from MySQL
df = spark.read \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "complaint") \
    .option("user", mysql_user) \
    .option("password", mysql_password) \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .load()

# 6. Category-wise analytics
category_counts = df.groupBy("category").count()

# 7. Sort by complaint count (highest first)
category_counts = category_counts.orderBy(
    "count",
    ascending=False
)


# 8. Display results
print("CATEGORY-WISE MYSQL COMPLAINT ANALYTICS")
category_counts.show()


# 9. Export analytics to CSV
output_path = project_folder / "output" / "mysql_category_analytics"
output_path.mkdir(parents=True, exist_ok=True)

csv_file = output_path / "category_analytics.csv"

rows = category_counts.collect()

with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["category", "count"])

    for row in rows:
        writer.writerow([row["category"], row["count"]])

print("Analytics exported successfully!")
print("CSV File Location:", csv_file)


# 10. Stop Spark
spark.stop()


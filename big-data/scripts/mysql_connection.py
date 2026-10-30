
import os
from pathlib import Path
from pyspark.sql import SparkSession

# 1. Locate MySQL JDBC Driver
project_folder = Path(__file__).resolve().parent.parent
jar_file = project_folder / "jars" / "mysql-connector-j-26.10.0.jar"

# 2. Read MySQL credentials from environment variables
mysql_user = os.getenv("DB_USERNAME")
mysql_password = os.getenv("DB_PASSWORD")

if not mysql_user or not mysql_password:
    raise ValueError("Please configure MYSQL_USER and MYSQL_PASSWORD.")

# 3. Create Spark Session and load JDBC Driver
spark = SparkSession.builder \
    .appName("SmartComplaintMySQLConnection") \
    .master("local[*]") \
    .config("spark.driver.extraClassPath", str(jar_file))  \
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

# 6. Display MySQL records
print("MYSQL DATA LOADED SUCCESSFULLY!")

df.show(5, truncate=False)

print("Total complaints in MySQL:", df.count())

# 7. Stop Spark
spark.stop()

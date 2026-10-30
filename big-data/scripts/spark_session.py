from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("SmartComplaintSystem") \
    .master("local[*]") \
    .getOrCreate()

print("Apache Spark started successfully!")

print("Spark Version:", spark.version)

# Stop Spark
spark.stop()
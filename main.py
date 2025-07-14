from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder.appName("BigDataTest").getOrCreate()

# Just print something
print("PySpark is working!")

# Stop the Spark session
spark.stop()
from pyspark.sql import SparkSession
import os

def get_spark_session():
    """Create and return a Spark session for local development."""

    # Set HADOOP_HOME if not set
    if 'HADOOP_HOME' not in os.environ:
        os.environ['HADOOP_HOME'] = 'C:\\hadoop'

    spark = SparkSession.builder \
        .appName("FinancialDataAggregator") \
        .master("local[1]") \
        .config("spark.driver.bindAddress", "127.0.0.1") \
        .config("spark.driver.host", "localhost") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")
    return spark

def stop_spark(spark):
    """Stop the Spark session."""
    spark.stop()

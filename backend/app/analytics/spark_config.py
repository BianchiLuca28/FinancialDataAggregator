from pyspark.sql import SparkSession

def get_spark_session():
    """Create and return a Spark session for local development."""
    spark = SparkSession.builder \
        .appName("FinancialDataAggregator") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark

def stop_spark(spark):
    """Stop the Spark session."""
    spark.stop()
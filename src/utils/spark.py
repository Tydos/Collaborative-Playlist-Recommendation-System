from pyspark.sql import SparkSession
from src.utils.config import load_config

def spark_session() -> SparkSession:
    config = load_config()

    driver_memory = config.get("spark_driver_memory", "8g")
    shuffle_partitions = config.get("spark_shuffle_partitions", 8)
    parquet_block_size = config.get("spark_parquet_block_size", 32 * 1024 * 1024)

    return (
        SparkSession.builder
        .appName("TrackETL")
        .config("spark.driver.memory", driver_memory)
        .config("spark.sql.shuffle.partitions", shuffle_partitions)
        .config("spark.sql.parquet.block.size", parquet_block_size)
        .getOrCreate()
    )
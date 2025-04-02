from pyspark.sql import SparkSession


def create_tables(
    spark,
    path="s3a://godata2023/delta",
    database: str = "godata2023",
):
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")
    spark.sql(f"DROP TABLE IF EXISTS {database}.trade")
    spark.sql(
        f"""
              CREATE TABLE {database}.trade (
                batch_id LONG,
                trade_timestamp TIMESTAMP,
                symbol STRING,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume INT,
                partition STRING
                ) USING DELTA
                PARTITIONED BY (partition)
                LOCATION '{path}/trade'
              """
    )
    
def drop_tables(
    spark,
    database: str = "godata2023",
):
    spark.sql(f"DROP TABLE IF EXISTS {database}.trade")
    spark.sql(f"DROP DATABASE IF EXISTS {database}")


if __name__ == '__main__':
    spark = SparkSession.builder \
    .appName("ddl") \
    .master('local[*]') \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.3.0,org.apache.hadoop:hadoop-aws:3.3.2") \
    .config("spark.databricks.delta.retentionDurationCheck.enabled", "false") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.hadoop.fs.s3a.access.key", "godata2023") \
    .config("spark.hadoop.fs.s3a.secret.key", "godata2023") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.region", "us-east-1") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .enableHiveSupport() \
    .getOrCreate()
    drop_tables(spark)
    create_tables(spark)

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
    spark = (
        SparkSession.builder.appName("{database}_ddl")
        .config("spark.executor.cores", "1")
        .config(
            "spark.executor.instances",
            "1",
        )
        .enableHiveSupport()
        .getOrCreate()
    )
    drop_tables(spark)
    create_tables(spark)

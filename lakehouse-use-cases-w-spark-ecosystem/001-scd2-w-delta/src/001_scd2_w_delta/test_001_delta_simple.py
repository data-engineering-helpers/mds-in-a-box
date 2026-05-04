#!/usr/bin/env python
#
# File: https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/data-processing/spark/examples/001-scd2-w-delta/src/001_scd2_w_delta/test_001_delta_simple.py
#

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import delta.tables as dt

from jobs import merge_customer_001_simple

#
k_spark_version = "4.1"
k_scala_version = "2.13"
k_dl_version = "4.2.0"
k_dl_jar_package = f"io.delta:delta-spark_{k_spark_version}_{k_scala_version}:{k_dl_version}"

#
schema_name = "bronze"
table_name = "dim_customer"
delta_table_name = f"{schema_name}.{table_name}"
cust_init_dataset = f"../data/{table_name}/init"
cust_full_dataset1 = f"../data/{table_name}/full1"

def getSparkSession() -> SparkSession:
    spark = (
        SparkSession.builder.appName("test-scd2-001-app")
        .config("spark.jars.packages", k_dl_jar_package)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .enableHiveSupport()
        .getOrCreate()
    )
    return spark

def test_merge_customer_001_simple():
    """
    Test that the job ingesting initial and full snapshot data sets
    """
    # Execute the ingestion job
    merge_customer_001_simple.main(argv=["--confs-dir", "confs", "--env", "local"])
    
    # Retrieve the Spark session
    spark = getSparkSession()

    # Retrieve the Delta table
    delta_table = dt.DeltaTable.forName(spark, delta_table_name)
    df_dt = delta_table.toDF()

    # After merging init (100 rows) with full1 (96 rows containing 42 changes and
    # 4 deletions), SCD2 should produce 142 rows in total.
    nb_rows_dt = df_dt.count()
    assert nb_rows_dt == 142

    # Historical rows are 42 replaced rows + 4 closed deletions.
    df_updated = df_dt.filter(df_dt.is_current == False)
    nb_rows_updated = df_updated.count()
    assert nb_rows_updated == 46

    # Current rows match the full1 snapshot size.
    df_current = df_dt.filter(df_dt.is_current == True)
    nb_rows_current = df_current.count()
    assert nb_rows_current == 96

    # Extraction date is mandatory in the upgraded schema.
    assert "extraction_date" in df_dt.columns

if __name__ == "__main__":
    test_merge_customer_001_simple()

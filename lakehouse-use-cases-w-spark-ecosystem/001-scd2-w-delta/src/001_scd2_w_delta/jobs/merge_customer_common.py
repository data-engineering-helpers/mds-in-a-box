#!/usr/bin/env python

import logging
import time
from dataclasses import dataclass
from typing import Any

import delta.tables as dt
import pyspark.sql
import pyspark.sql.functions as F

try:
    from .job_config import ConfigLoader, JobArgs
except ImportError:
    from job_config import ConfigLoader, JobArgs


BUSINESS_COLUMNS = [
    "uuid",
    "name",
    "username",
    "mail",
    "ssn",
    "company",
    "job",
    "address",
    "residence",
    "birthdate",
    "sex",
    "blood_group",
    "website",
    "current_location_lat",
    "current_location_lon",
]


@dataclass
class JobRuntimeConfig:
    job_name: str
    table_name: str
    spark_conf: dict[str, Any]
    datasets_conf: dict[str, Any]
    log_level: str


def _build_logger(log_level: str) -> logging.Logger:
    logger = logging.getLogger("merge_customer")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [merge_customer] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    return logger


def _build_spark_session(job_name: str, spark_conf: dict[str, Any]) -> pyspark.sql.SparkSession:
    app_name = spark_conf.get("app_name", job_name)
    builder = pyspark.sql.SparkSession.builder.appName(app_name)

    remote = spark_conf.get("remote")
    if remote:
        builder = builder.remote(remote)

    configs_dict = spark_conf.get("configs", {})
    for key, value in configs_dict.items():
        builder = builder.config(key, str(value))

    enable_hive = spark_conf.get("enable_hive_support", False)
    if enable_hive:
        builder = builder.enableHiveSupport()

    spark_session = builder.getOrCreate()
    logger = logging.getLogger("merge_customer")
    session_type = f"remote ({remote})" if remote else "local"
    logger.debug(
        "Spark session created: app_name=%s, type=%s, hive_support=%s, config_count=%d",
        app_name,
        session_type,
        enable_hive,
        len(configs_dict),
    )
    return spark_session


def _read_input_dataset(spark: pyspark.sql.SparkSession, dataset_conf: dict[str, Any]) -> pyspark.sql.DataFrame:
    logger = logging.getLogger("merge_customer")
    
    if "table" in dataset_conf:
        table_name = dataset_conf["table"]
        logger.debug("Reading dataset from table: %s", table_name)
        return spark.table(table_name)

    fmt = dataset_conf.get("format", "parquet")
    path = dataset_conf["path"]
    options_dict = dataset_conf.get("options", {})
    
    logger.debug("Reading dataset from path: %s, format=%s, options_count=%d", path, fmt, len(options_dict))
    reader = spark.read.format(fmt)
    for key, value in options_dict.items():
        reader = reader.option(key, value)
    return reader.load(path)


def _add_scd2_metadata(df: pyspark.sql.DataFrame, start_date_days_offset: int = 0) -> pyspark.sql.DataFrame:
    if start_date_days_offset > 0:
        start_date_expr = F.date_sub(F.current_date().cast("date"), days=start_date_days_offset)
    else:
        start_date_expr = F.current_date().cast("date")

    return (
        df.withColumn("start_date", start_date_expr)
        .withColumn("end_date", F.lit("9999-12-31").cast("date"))
        .withColumn("is_current", F.lit(True))
    )


def _display_table_head(spark: pyspark.sql.SparkSession, table_name: str, logger: logging.Logger) -> None:
    df_table = spark.sql(f"select * from {table_name}")
    row_count = df_table.count()
    logger.info("%s row count=%s", table_name, row_count)
    df_table.show(5, truncate=False)


def _process_initial_snapshot(
    spark: pyspark.sql.SparkSession,
    table_name: str,
    datasets_conf: dict[str, Any],
    logger: logging.Logger,
) -> None:
    logger.info("=== Processing initial snapshot for table: %s ===", table_name)
    
    init_datasets_conf = datasets_conf["inputs"]["init"]
    logger.debug("Initial dataset config: %s", init_datasets_conf)
    
    read_start_time = time.time()
    source_df = _read_input_dataset(spark, init_datasets_conf)
    
    start_date_days_offset = int(datasets_conf.get("start_date_days_offset", 0))
    logger.debug("Adding SCD2 metadata with start_date_days_offset=%d", start_date_days_offset)
    source_df = _add_scd2_metadata(
        source_df,
        start_date_days_offset=start_date_days_offset,
    )
    
    source_count = source_df.count()
    read_elapsed = time.time() - read_start_time
    logger.info(
        "Initial snapshot loaded: row_count=%d, elapsed=%.2fs",
        source_count,
        read_elapsed,
    )

    table_exists = True
    try:
        dt.DeltaTable.forName(spark, table_name)
    except Exception:
        table_exists = False

    if table_exists:
        logger.info("Table %s exists; will be replaced with initial snapshot", table_name)
    else:
        logger.info("Table %s does not exist; creating new table", table_name)

    write_start_time = time.time()
    source_df.write.format("delta").mode("overwrite").saveAsTable(table_name)
    write_elapsed = time.time() - write_start_time
    logger.info(
        "Initial snapshot written: table=%s, elapsed=%.2fs",
        table_name,
        write_elapsed,
    )
    
    _display_table_head(spark, table_name, logger)


def _scd2_merge_incremental(
    spark: pyspark.sql.SparkSession,
    table_name: str,
    datasets_conf: dict[str, Any],
    logger: logging.Logger,
) -> None:
    logger.info("=== Processing SCD2 incremental merge for table: %s ===", table_name)
    
    inc_datasets_conf = datasets_conf["inputs"]["incremental"]
    logger.debug("Incremental dataset config: %s", inc_datasets_conf)
    
    read_start_time = time.time()
    inc_df = _read_input_dataset(spark, inc_datasets_conf)
    inc_count = inc_df.count()
    read_elapsed = time.time() - read_start_time
    logger.info(
        "Incremental dataset loaded: row_count=%d, elapsed=%.2fs",
        inc_count,
        read_elapsed,
    )

    delta_table = dt.DeltaTable.forName(spark, table_name)
    target_df = delta_table.toDF()
    target_count = target_df.count()
    logger.debug("Target table %s current row count: %d", table_name, target_count)

    changed_rows = (
        inc_df.alias("src")
        .join(target_df.alias("tgt"), on="uuid", how="inner")
        .where("tgt.is_current = true AND (src.company != tgt.company OR src.job != tgt.job)")
        .select("src.*")
    )

    changed_count = changed_rows.count()
    logger.info(
        "Data quality check: incremental=%d, target_current=%d, changed_rows=%d",
        inc_count,
        target_count,
        changed_count,
    )

    changed_with_null_merge_key = changed_rows.selectExpr("NULL as mergeKey", "*")
    incoming_with_merge_key = inc_df.selectExpr("uuid as mergeKey", "*")
    staged_updates = changed_with_null_merge_key.union(incoming_with_merge_key)

    staged_count = staged_updates.count()
    logger.debug(
        "Staged updates prepared: changed_with_null_key=%d, incoming_with_uuid=%d, total_staged=%d",
        changed_count,
        inc_count,
        staged_count,
    )

    insert_values = {col: F.col(f"stgupd.{col}") for col in BUSINESS_COLUMNS}
    insert_values.update(
        {
            "start_date": F.current_date().cast("date"),
            "end_date": F.lit("9999-12-31").cast("date"),
            "is_current": F.lit(True),
        }
    )

    logger.info("Executing SCD2 merge: matched_updates will close old records, unmatched_inserts will add new")
    merge_start_time = time.time()
    (
        delta_table.alias("tgt")
        .merge(staged_updates.alias("stgupd"), "tgt.uuid = stgupd.mergeKey")
        .whenMatchedUpdate(
            condition="tgt.is_current = true AND (tgt.company != stgupd.company OR tgt.job != stgupd.job)",
            set={
                "is_current": F.lit(False),
                "end_date": F.current_date(),
            },
        )
        .whenNotMatchedInsert(values=insert_values)
        .execute()
    )
    merge_elapsed = time.time() - merge_start_time
    logger.info("SCD2 merge completed: elapsed=%.2fs", merge_elapsed)

    _display_table_head(spark, table_name, logger)


def load_runtime_config(job_name: str, args: JobArgs) -> JobRuntimeConfig:
    loader = ConfigLoader(args.confs_dir, env=args.env)
    spark_config_map = loader.get("spark.yml")
    datasets_config_map = loader.get("datasets.yml")

    if job_name not in spark_config_map:
        raise KeyError(f"Missing spark config for job '{job_name}'")
    if job_name not in datasets_config_map:
        raise KeyError(f"Missing dataset config for job '{job_name}'")

    datasets_conf = datasets_config_map[job_name]
    if "table" not in datasets_conf:
        raise KeyError(f"Missing 'table' key in datasets config for job '{job_name}'")

    table_name = datasets_conf["table"]
    spark_conf = spark_config_map[job_name]

    return JobRuntimeConfig(
        job_name=job_name,
        table_name=table_name,
        spark_conf=spark_conf,
        datasets_conf=datasets_conf,
        log_level=args.log_level,
    )


def run_customer_merge_job(job_name: str, argv: list[str] | None = None) -> None:
    job_start_time = time.time()
    
    args = JobArgs.parse_common_args(argv)
    runtime = load_runtime_config(job_name, args)
    logger = _build_logger(runtime.log_level)

    logger.info("\n" + "="*80)
    logger.info("SCD2 Customer Merge ETL Pipeline Starting")
    logger.info("="*80)
    
    job_name_runtime = runtime.job_name
    confs_dir_path = args.confs_dir
    env_name = args.env
    log_level_str = runtime.log_level
    table_name = runtime.table_name
    
    logger.info(
        "Configuration: job=%s, confs_dir=%s, env=%s, log_level=%s, table=%s",
        job_name_runtime,
        confs_dir_path,
        env_name,
        log_level_str,
        table_name,
    )
    logger.debug("Spark config keys: %s", list(runtime.spark_conf.keys()))
    logger.debug("Dataset config keys: %s", list(runtime.datasets_conf.keys()))

    spark_build_start = time.time()
    spark = _build_spark_session(runtime.job_name, runtime.spark_conf)
    spark_build_elapsed = time.time() - spark_build_start
    logger.info("Spark session created: elapsed=%.2fs", spark_build_elapsed)
    
    try:
        spark.sparkContext.setLogLevel(runtime.log_level)
        logger.debug("Spark Context log level set to: %s", runtime.log_level)
    except Exception:
        # Spark Connect sessions do not expose sparkContext.
        logger.debug("sparkContext not available; skipping SparkContext log-level setup")

    datasets_conf = runtime.datasets_conf

    _process_initial_snapshot(
        spark=spark,
        table_name=table_name,
        datasets_conf=datasets_conf,
        logger=logger,
    )

    _scd2_merge_incremental(
        spark=spark,
        table_name=table_name,
        datasets_conf=datasets_conf,
        logger=logger,
    )

    total_elapsed = time.time() - job_start_time
    logger.info("="*80)
    logger.info(
        "SCD2 Customer Merge ETL Pipeline Finished: job=%s, total_elapsed=%.2fs",
        job_name_runtime,
        total_elapsed,
    )
    logger.info("="*80 + "\n")

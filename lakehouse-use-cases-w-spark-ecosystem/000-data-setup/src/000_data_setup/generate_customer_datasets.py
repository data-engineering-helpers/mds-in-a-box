#!/usr/bin/env python
#
# File: https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/data-processing/spark/examples/000_data_setup/src/000_data_setup/generate_customer_datasets.py
#

import argparse
from datetime import date, datetime, timedelta

from faker import Faker
from pyspark.sql import DataFrame, SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T

DATASET_PATHS = {
    "init": "../data/dim_customer/init",
    "full1": "../data/dim_customer/full1",
    "full2": "../data/dim_customer/full2",
    "delta1": "../data/dim_customer/delta1",
    "delta2": "../data/dim_customer/delta2",
}

CUSTOMER_COLUMNS = [
    "uuid",
    "address",
    "birthdate",
    "blood_group",
    "company",
    "job",
    "mail",
    "name",
    "residence",
    "sex",
    "ssn",
    "username",
    "website",
    "current_location_lat",
    "current_location_lon",
    "extraction_date",
]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate deterministic sample datasets for SCD2 tutorials.",
    )
    parser.add_argument("--faker-seed", type=int, default=4321)
    parser.add_argument("--init-count", type=int, default=100)
    parser.add_argument("--full1-change-count", type=int, default=42)
    parser.add_argument("--full1-delete-count", type=int, default=4)
    parser.add_argument("--full2-change-count", type=int, default=40)
    parser.add_argument("--full2-additional-delete-count", type=int, default=6)
    parser.add_argument("--init-extraction-date", type=str, default=None)
    parser.add_argument("--snapshot-extraction-date", type=str, default=None)
    return parser.parse_args(argv)


def _parse_iso_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def _resolve_dates(args: argparse.Namespace) -> tuple[date, date]:
    snapshot_date = (
        _parse_iso_date(args.snapshot_extraction_date)
        if args.snapshot_extraction_date
        else date.today()
    )
    init_date = (
        _parse_iso_date(args.init_extraction_date)
        if args.init_extraction_date
        else snapshot_date - timedelta(days=7)
    )
    return init_date, snapshot_date


def _validate_counts(args: argparse.Namespace) -> None:
    if args.init_count <= 0:
        raise ValueError("--init-count must be strictly positive")
    if args.full1_change_count < 0 or args.full1_delete_count < 0:
        raise ValueError("full1 change/delete counts must be non-negative")
    if args.full2_change_count < 0 or args.full2_additional_delete_count < 0:
        raise ValueError("full2 change/delete counts must be non-negative")
    if args.full1_change_count + args.full1_delete_count > args.init_count:
        raise ValueError("full1 change + delete counts exceed init count")


def _set_extraction_date(df: DataFrame, extraction_date: date) -> DataFrame:
    return df.withColumn("extraction_date", F.lit(extraction_date.isoformat()).cast("date"))


def _to_customer_schema(df: DataFrame) -> DataFrame:
    return df.select(*CUSTOMER_COLUMNS)


def _write_dataset(df: DataFrame, dataset_name: str) -> int:
    path = DATASET_PATHS[dataset_name]
    df_out = _to_customer_schema(df)
    (
        df_out.coalesce(1)
        .write.mode("overwrite")
        .partitionBy("extraction_date")
        .parquet(path)
    )
    row_count = df_out.count()
    print(f"{dataset_name}: row_count={row_count} path={path}")
    return row_count


def _mutate_company_job(
    spark: SparkSession,
    base_df: DataFrame,
    uuids: list[str],
    faker_seed: int,
) -> DataFrame:
    if not uuids:
        return base_df

    faker_local = Faker()
    faker_local.seed_instance(faker_seed)
    sorted_uuids = sorted(set(uuids))
    mutation_rows = [
        (uuid, faker_local.company(), faker_local.job())
        for uuid in sorted_uuids
    ]
    mutation_df = spark.createDataFrame(
        mutation_rows,
        schema="uuid string, company_new string, job_new string",
    )

    return (
        base_df.alias("src")
        .join(mutation_df.alias("mut"), on="uuid", how="left")
        .withColumn("company", F.coalesce(F.col("mut.company_new"), F.col("src.company")))
        .withColumn("job", F.coalesce(F.col("mut.job_new"), F.col("src.job")))
        .select(
            "src.uuid",
            "src.address",
            "src.birthdate",
            "src.blood_group",
            "company",
            "job",
            "src.mail",
            "src.name",
            "src.residence",
            "src.sex",
            "src.ssn",
            "src.username",
            "src.website",
            "src.current_location_lat",
            "src.current_location_lon",
            "src.extraction_date",
        )
    )


def _extract_sorted_uuids(df: DataFrame) -> list[str]:
    return [row.uuid for row in df.select("uuid").orderBy("uuid").collect()]


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    _validate_counts(args)
    init_extraction_date, snapshot_extraction_date = _resolve_dates(args)

    spark = SparkSession.builder.appName("scd2-app").getOrCreate()

    faker = Faker()
    faker.seed_instance(args.faker_seed)

    cust_profiles = [
        faker.profile() | {"uuid": faker.uuid4()}
        for _ in range(args.init_count)
    ]
    df_customer_init = spark.createDataFrame(cust_profiles)

    df_customer_init = df_customer_init.withColumn(
        "current_location_lat",
        F.col("current_location._1").cast("double"),
    )
    df_customer_init = df_customer_init.withColumn(
        "current_location_lon",
        F.col("current_location._2").cast("double"),
    )
    df_customer_init = df_customer_init.drop("current_location")

    udf_website = F.udf(lambda x: x[0], T.StringType())
    df_customer_init = df_customer_init.withColumn("website", udf_website(df_customer_init.website))
    df_customer_init = _set_extraction_date(df_customer_init, init_extraction_date)
    df_customer_init = _to_customer_schema(df_customer_init)

    init_row_count = _write_dataset(df_customer_init, "init")

    init_uuids = _extract_sorted_uuids(df_customer_init)
    full1_changed_uuids = init_uuids[: args.full1_change_count]
    full1_deleted_uuids = init_uuids[
        args.full1_change_count : args.full1_change_count + args.full1_delete_count
    ]
    full1_excluded_uuids = full1_changed_uuids + full1_deleted_uuids

    df_full1_changed = df_customer_init.filter(F.col("uuid").isin(full1_changed_uuids))
    df_full1_changed = _mutate_company_job(
        spark,
        df_full1_changed,
        full1_changed_uuids,
        faker_seed=args.faker_seed + 1,
    )
    df_full1_changed = _set_extraction_date(df_full1_changed, snapshot_extraction_date)
    df_delta1 = _to_customer_schema(df_full1_changed)

    df_full1_unchanged = df_customer_init.filter(~F.col("uuid").isin(full1_excluded_uuids))
    df_full1_unchanged = _set_extraction_date(df_full1_unchanged, snapshot_extraction_date)
    df_full1 = _to_customer_schema(df_full1_unchanged.unionByName(df_delta1))

    delta1_row_count = _write_dataset(df_delta1, "delta1")
    full1_row_count = _write_dataset(df_full1, "full1")

    full1_uuids = _extract_sorted_uuids(df_full1)
    if args.full2_change_count + args.full2_additional_delete_count > len(full1_uuids):
        raise ValueError("full2 change + delete counts exceed full1 row count")

    full2_changed_uuids = full1_uuids[: args.full2_change_count]
    full2_deleted_uuids = full1_uuids[
        args.full2_change_count : args.full2_change_count + args.full2_additional_delete_count
    ]
    full2_excluded_uuids = full2_changed_uuids + full2_deleted_uuids

    df_full2_changed = df_full1.filter(F.col("uuid").isin(full2_changed_uuids))
    df_full2_changed = _mutate_company_job(
        spark,
        df_full2_changed,
        full2_changed_uuids,
        faker_seed=args.faker_seed + 2,
    )
    df_full2_changed = _set_extraction_date(df_full2_changed, snapshot_extraction_date)
    df_delta2 = _to_customer_schema(df_full2_changed)

    df_full2_unchanged = df_full1.filter(~F.col("uuid").isin(full2_excluded_uuids))
    df_full2_unchanged = _set_extraction_date(df_full2_unchanged, snapshot_extraction_date)
    df_full2 = _to_customer_schema(df_full2_unchanged.unionByName(df_delta2))

    delta2_row_count = _write_dataset(df_delta2, "delta2")
    full2_row_count = _write_dataset(df_full2, "full2")

    expected_full1_count = args.init_count - args.full1_delete_count
    expected_full2_count = expected_full1_count - args.full2_additional_delete_count

    assert init_row_count == args.init_count
    assert delta1_row_count == args.full1_change_count
    assert full1_row_count == expected_full1_count
    assert delta2_row_count == args.full2_change_count
    assert full2_row_count == expected_full2_count


if __name__ == "__main__":
    main()

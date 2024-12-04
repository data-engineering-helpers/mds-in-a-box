Modern Data Stack (MDS) in a box
================================

# Table of Content (ToC)
* [Overview](#overview)
* [References](#references)
* [Articles](#articles)
  * [The SwirlAI data engineering project](#the-swirlai-data-engineering-project)
* [Frameworks](#frameworks)
  * [Minio](#minio)
  * [LakeFS](#lakefs)
  * [PostgreSQL](#postgresql)
  * [DuckDB](#duckdb)
* [End\-to\-end projects](#end-to-end-projects)
  * [Bike sharing](#bike-sharing)
  * [Car price predictor](#car-price-predictor)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)

# Overview
[This project](https://github.com/data-engineering-helpers/mds-in-a-box)
intends to gather referential material and to give practical hints
on how to reproduce locally all-in-one modern data stack (MDS).

Among other use cases, we may think of training, onboarding newcomers,
testing/benchmarking some new components (_e.g._, Delta Lake vs Iceberg
vs Hudi), LakeFS.

Even though the members of the GitHub organization may be employed by
some companies, they speak on their personal behalf and do not represent
these companies.

# References
* [Architecture principles for data engineering pipelines on the Modern Data Stack (MDS)](https://github.com/data-engineering-helpers/architecture-principles)
  + [Material for the Data platform - Architecture principles](https://github.com/data-engineering-helpers/architecture-principles/blob/main/material/README.md)
* Specifications/principles for a
  [data engineering pipeline deployment tool](https://github.com/data-engineering-helpers/data-pipeline-deployment)
  + [`dpcctl`, the Data Processing Pipeline (DPP) CLI utility](https://github.com/data-engineering-helpers/dppctl), a Minimal Viable Product (MVP) in Go
* [Material for the Data platform - Data-lakes, data warehouses, data lake-houses](https://github.com/data-engineering-helpers/data-lakehouse)
* [Material for the Data platform - Data life cycle](https://github.com/data-engineering-helpers/data-life-cycle/blob/main/README.md)
* [Material for the Data platform - Data contracts](https://github.com/data-engineering-helpers/data-contracts/blob/main/README.md)
* [Material for the Data platform - Metadata](https://github.com/data-engineering-helpers/metadata/blob/main/README.md)
* [Material for the Data platform - Data quality](https://github.com/data-engineering-helpers/data-quality/blob/main/README.md)
* [Material for the Data platform - Cheat sheets](https://github.com/data-engineering-helpers/ks-cheat-sheets)

# Articles

## The SwirlAI data engineering project
* Title: The SwirlAI data engineering project
* Author: Aurimas Griciūnas
  ([Aurimas Griciūnas on LinkedIn](https://www.linkedin.com/in/aurimas-griciunas/), [Aurimas Griciūnas on Substck](https://substack.com/@swirlai))
* Date: July 2023
* Link on Substack: https://www.newsletter.swirlai.com/p/the-swirlai-data-engineering-project

# Frameworks

## Minio
* See also
  [GitHub - Data Engineering Helpers - Knowledge Sharing - Minio](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/frameworks/minio/README.md)

## LakeFS
* Reference:
  https://lakefs.io/blog/the-docker-everything-bagel-spin-up-a-local-data-stack/
* See also
  [GitHub - Data Engineering Helpers - Knowledge Sharing - LakeFS](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/frameworks/lakefs/README.md)

## PostgreSQL
* See also
  [GitHub - Data Engineering Helpers - Knowledge Sharing - PostgreSQL](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/db/postgresql/README.md)

## DuckDB
* Reference:
  https://duckdb.org/2022/10/12/modern-data-stack-in-a-box.html
* See also
  [GitHub - Data Engineering Helpers - Knowledge Sharing - DuckDB](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/db/duckdb/README.md)
* DuckDB home page: https://duckdb.org/
   + Why DuckDB: https://duckdb.org/why_duckdb
* DuckDB project on GitHub: https://github.com/duckdb/duckdb

# End-to-end projects

## Bike sharing
* Post on LinkedIn: https://www.linkedin.com/posts/pau-labarta-bajo-4432074b_machinelearning-mlops-realworldml-ugcPost-7265607334830256128-ZkrV/
  * Authors: Paul Labarta Bajo and Javier Yanzon
    ([Paul Labarta Bajo on LinkedIn](https://www.linkedin.com/in/pau-labarta-bajo-4432074b/),
    [Javier Yanzon on LinkedIn](https://www.linkedin.com/in/javieryanzon/))
* GitHub repository: https://github.com/javieryanzon/bike_sharing_demand_predictor

## Car price predictor
* Article: https://medium.com/towards-data-engineering/predicting-car-prices-with-fastapi-streamlit-mlflow-kafka-and-debezium-a-practical-7084d5673c0e
* Author: Stefen Taime
  ([Stefen Taime on LinkedIn](https://www.linkedin.com/in/stefen-taime-829492117/))
* GitHub repository: https://github.com/Stefen-Taime/car-price-predictor


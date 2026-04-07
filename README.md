# Modern Data Stack (MDS) in a box

## Table of Content (ToC)

* [Modern Data Stack (MDS) in a box](#modern-data-stack-mds-in-a-box)
  * [Table of Content (ToC)](#table-of-content-toc)
  * [Overview](#overview)
  * [References](#references)
  * [Articles](#articles)
    * [The SwirlAI data engineering project](#the-swirlai-data-engineering-project)
  * [Frameworks](#frameworks)
    * [SeaweedFS](#seaweedfs)
    * [PostgreSQL](#postgresql)
    * [DuckDB](#duckdb)
    * [Alternative frameworks](#alternative-frameworks)
  * [Minio](#minio)
  * [LakeFS](#lakefs)
  * [End\-to\-end projects](#end-to-end-projects)
    * [Build a local open data lakehouse](#build-a-local-open-data-lakehouse)
    * [Building an End\-to\-end MLOps Project with Databricks](#building-an-end-to-end-mlops-project-with-databricks)
    * [Bike sharing](#bike-sharing)
  * [Car price predictor](#car-price-predictor)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)

## Overview

[This project](https://github.com/data-engineering-helpers/mds-in-a-box)
intends to gather referential material and to give practical hints
on how to reproduce locally all-in-one modern data stack (MDS).

Among other use cases, we may think of training, onboarding newcomers,
testing/benchmarking some new components (_e.g._, Delta Lake vs Iceberg
vs Hudi), LakeFS.

Even though the members of the GitHub organization may be employed by
some companies, they speak on their personal behalf and do not represent
these companies.

## References

* [Architecture principles for data engineering pipelines on the Modern Data Stack (MDS)](https://github.com/data-engineering-helpers/architecture-principles)
  * [Material for the Data platform - Architecture principles](https://github.com/data-engineering-helpers/architecture-principles/blob/main/material/README.md)
* Specifications/principles for a
  [data engineering pipeline deployment tool](https://github.com/data-engineering-helpers/data-pipeline-deployment)
  * [`dpcctl`, the Data Processing Pipeline (DPP) CLI utility](https://github.com/data-engineering-helpers/dppctl),
  a Minimal Viable Product (MVP) in Go
* [Material for the Data platform - Data-lakes, data warehouses, data lake-houses](https://github.com/data-engineering-helpers/data-lakehouse)
* [Material for the Data platform - Data life cycle](https://github.com/data-engineering-helpers/data-life-cycle/blob/main/README.md)
* [Material for the Data platform - Data contracts](https://github.com/data-engineering-helpers/data-contracts/blob/main/README.md)
* [Material for the Data platform - Metadata](https://github.com/data-engineering-helpers/metadata/blob/main/README.md)
* [Material for the Data platform - Data quality](https://github.com/data-engineering-helpers/data-quality/blob/main/README.md)
* [Material for the Data platform - Cheat sheets](https://github.com/data-engineering-helpers/ks-cheat-sheets)

## Articles

### The SwirlAI data engineering project

* Title: The SwirlAI data engineering project
* Author: Aurimas Griciūnas
  ([Aurimas Griciūnas on LinkedIn](https://www.linkedin.com/in/aurimas-griciunas/),
  [Aurimas Griciūnas on Substck](https://substack.com/@swirlai))
* Date: July 2023
* [Link on Substack](https://www.newsletter.swirlai.com/p/the-swirlai-data-engineering-project)

## Frameworks

### SeaweedFS

### PostgreSQL

* See also
  [GitHub - Data Engineering Helpers - Knowledge Sharing - PostgreSQL](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/db/postgresql/README.md)

### DuckDB

* See also
  [GitHub - Data Engineering Helpers - Knowledge Sharing - DuckDB](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/db/duckdb/README.md)
* [DuckDB blog - MDS in a box](https://duckdb.org/2022/10/12/modern-data-stack-in-a-box.html)
* [DuckDB home page](https://duckdb.org/)
  * [Why DuckDB](https://duckdb.org/why_duckdb)
* [DuckDB project on GitHub](https://github.com/duckdb/duckdb)

### Alternative frameworks

## Minio

* See also
  [GitHub - Data Engineering Helpers - Knowledge Sharing - Minio](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/frameworks/minio/README.md)

## LakeFS

* [LakeFS blog - Spin up a local data stack](https://lakefs.io/blog/the-docker-everything-bagel-spin-up-a-local-data-stack/)
* See also
  [GitHub - Data Engineering Helpers - Knowledge Sharing - LakeFS](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/frameworks/lakefs/README.md)

## End-to-end projects

### Build a local open data lakehouse

* Title: Build a local open data lakehouse with k3d, Apache Ozone,
  Apache Polaris and Trino
* Articles:
  * [Medium - Build a local open data lakehouse](https://medium.com/@cyancg/build-a-local-open-data-lakehouse-with-k3d-apache-ozone-apache-polaris-and-trino-cbe3adf8ad57)
    * Date: Apr. 2026
  * [Medium - Deploying Keycloak and Superset](https://medium.com/@cyancg/deploying-keycloak-and-apache-superset-on-k3d-with-sso-2531ee52c658)
* Author: Cheng Guan Poh
  ([Cheng Guan Poh on LinkedIn](https://www.linkedin.com/in/cgpoh/),
  [Cheng Guan Poh on Medium](https://medium.com/@cyancg))
* Overview:

> Spin up a fully integrated, locally-running open data lakehouse on your laptop
> in under 30 minutes using Kubernetes in Docker (k3d), Apache Ozone as S3-compatible
> object storage, Apache Polaris as the Iceberg REST catalog and Trino as
> the SQL query engine. No cloud account required.

### Building an End-to-end MLOps Project with Databricks

* [Medium - Building an End-to-end MLOps Project with Databricks](https://medium.com/marvelous-mlops/building-an-end-to-end-mlops-project-with-databricks-8cd9a85cc3c0)
* Author: Benito Martin
  ([Benito Martin on LinkedIn](https://www.linkedin.com/in/benitomzh/),
  [Benito Martin on  Medium](https://medium.com/@benitomartin))

This blog post details a capstone project using Databricks for MLOps. It covers
the end-to-end process of deploying a machine learning model, from data
preprocessing and feature engineering to model monitoring and continuous
integration/continuous deployment (CI/CD). Key learnings include:

* Databricks for MLOps:  Using Databricks for data preprocessing, feature
  engineering, model training, and deployment.
* Feature Store: Leveraging Databricks Feature Store for consistent feature
  computation.
* MLflow Tracking: Tracking experiments, logging parameters and metrics, and
  ensuring reproducibility.
* Model Serving: Exploring different model serving architectures for efficient
  deployment.
* A/B Testing: Implementing A/B testing for model comparison and
  performance-based routing.
* Databricks Asset Bundles: Managing projects with Infrastructure-as-Code (IaC)
  principles.
* Monitoring and Drift Detection: Setting up model monitoring, tracking metrics,
  and detecting drift.
* CI/CD: Implementing CI/CD workflows for continuous model validation and
  deployment.
* Scalability: Scaling models for production and real-time serving.

### Bike sharing

* [Post on LinkedIn](https://www.linkedin.com/posts/pau-labarta-bajo-4432074b_machinelearning-mlops-realworldml-ugcPost-7265607334830256128-ZkrV/)
  * Authors: Paul Labarta Bajo and Javier Yanzon
    ([Paul Labarta Bajo on LinkedIn](https://www.linkedin.com/in/pau-labarta-bajo-4432074b/),
    [Javier Yanzon on LinkedIn](https://www.linkedin.com/in/javieryanzon/))
* [GitHub - Bike sharing demand predictor](https://github.com/javieryanzon/bike_sharing_demand_predictor)

## Car price predictor

* [Medium - Predicting car prices](https://medium.com/towards-data-engineering/predicting-car-prices-with-fastapi-streamlit-mlflow-kafka-and-debezium-a-practical-7084d5673c0e)
* Author: Stefen Taime
  ([Stefen Taime on LinkedIn](https://www.linkedin.com/in/stefen-taime-829492117/))
* [GitHub - Car price predictor](https://github.com/Stefen-Taime/car-price-predictor)

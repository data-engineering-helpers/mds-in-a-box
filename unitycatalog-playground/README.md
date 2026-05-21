# Modern Data Stack (MDS) in a box - Unity Catalog (UC) playground

## Table of Content (ToC)

* [Modern Data Stack (MDS) in a box](#modern-data-stack-mds-in-a-box)
  * [Table of Content (ToC)](#table-of-content-toc)
  * [Overview](#overview)
  * [Stack](#stack)
  * [Requirements](#requirements)
  * [References](#references)
    * [Doc \- Docker](#doc---docker)
    * [Doc \- Unity Catalog](#doc---unity-catalog)
    * [Doc \- AWS CLI](#doc---aws-cli)
  * [Getting Started](#getting-started)
    * [Start the Lakehouse](#start-the-lakehouse)
    * [Interact with (SeaweedFS\-powered) S3](#interact-with-seaweedfs-powered-s3)
    * [Interact with Unity Catalog (UC)](#interact-with-unity-catalog-uc)
    * [Stop the Lakehouse](#stop-the-lakehouse)
  * [Setup](#setup)
    * [Docker ecosystem](#docker-ecosystem)
    * [Unity Catalog client](#unity-catalog-client)
    * [AWS CLI](#aws-cli)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)

## Overview

[This section](https://github.com/data-engineering-helpers/mds-in-a-box/tree/main/unitycatalog-playground/)
is part of the
[Modern Data Stack (MDS) in a box Knowledge Sharing (KS) repository](https://github.com/data-engineering-helpers/mds-in-a-box)
and showcases a fully open-source, self-hostable data lakehouse for local
development and testing of modern data workflows. It features production-grade
infrastructure on a laptop with Unity Catalog, the Apache Spark ecosystem
(Spark, Spark Connect, Delta Lake, Delta Connect), and Kafka - no cloud account
required. In the future, it will include a realistic data generation framework
to test batch and streaming pipelines.

### Why Unity Catalog playground?

* **Learn** data engineering with real tools, not toy examples
* **Develop** and test Spark jobs locally before deploying to production
* **Experiment** with Delta Lake table formats, streaming pipelines, and
  medallion architecture
* **Deploy** (optional) to a cloud provider when ready using
  [Databricks Declarative Automation Bundles (DAB)](https://docs.databricks.com/aws/en/dev-tools/bundles/)

## Stack

| Component | Version | Purpose |
|-----------|---------|---------|

| Unity Catalog | 0.4.0 | REST catalog (optional) |
| Apache Spark | 4.1 / 4.2 | Distributed compute |
| Delta Lake | 4.1 / 4.2 | ACID table format (optional) |
| SeaweedFS | - | S3-compatible storage (optional) |
| Apache Airflow | 3.1 | Workflow orchestration (optional) |
| Apache Kafka | 3.6 | Event streaming (optional) |
| PostgreSQL | 18 | Catalog metadata (optional) |

## Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|

| RAM | 8 GB | 16 GB |
| Disk | 20 GB | 50 GB |
| CPU | 4 cores | 8 cores |

**Software**: Docker, Java 21+, Python 3.12+

## References

* [Material for the Data platform - Modern Data Stack (MDS) in a box](https://github.com/data-engineering-helpers/mds-in-a-box)
* [GitHub - Unity Catalog playground](https://github.com/newfront/unitycatalog-playground)
* [GitHub - Lakehouse at home](https://github.com/lisancao/lakehouse-at-home)
* Author: Lisa N. Cao
  ([Lisa N. Cao on LinkedIn](https://www.linkedin.com/in/lisancao/),
  [Lisa N. Cao on GitHub](https://github.com/lisancao))
* [Medium - Declarative Pipelining in Apache Spark Part 1](https://medium.com/apache-spark/declarative-pipelining-in-apache-spark-part-1-focus-on-your-data-not-your-dags-553a1056d178),
  March 2026

### Doc - Docker

* [Rancher Desktop](https://rancherdesktop.io/)
  * [GitHub - Rancher Desktop](https://github.com/rancher-sandbox/rancher-desktop/)
  * [Rancher Desktop doc - Install on Linux](https://docs.rancherdesktop.io/getting-started/installation/#linux)
* [Docker doc - Getting Started](https://www.docker.com/get-started/)
  * [Docker doc - Install Docker Compose on Linux](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually)

### Doc - Unity Catalog

* [Unity Catalog (UC) home page](https://www.unitycatalog.io/)
* [GitHub - Unity Catalog (UC) repository](https://github.com/unitycatalog/unitycatalog/)
  * [GitHub - UC - CLI usage](https://github.com/unitycatalog/unitycatalog/blob/main/docs/usage/cli.md)
  * [GitHub - UC - AWS configuration](https://github.com/unitycatalog/unitycatalog/blob/main/docs/server/aws.md)
* [UC blog - Unity Catalog 101](https://www.unitycatalog.io/blogs/unity-catalog-oss)
  * [UC blog - How to use the Unity Catalog REST API](https://www.unitycatalog.io/blogs/how-to-use-the-unity-catalog-rest-api)
  * [Unity Catalog REST API - OpenAPI](https://github.com/unitycatalog/unitycatalog/blob/main/api/all.yaml)
  * [UC blog - Introducing Unity Catalog Managed Tables](https://www.unitycatalog.io/blogs/introducing-unity-catalog-managed-tables)

### Doc - AWS CLI

* [AWS Doc - What is the AWS Command Line Interface?](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
* [AWS Doc - Installing or updating to the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

## Getting Started

* Potentially adjust the
  [`etc/conf/s3.json` S3 configuration file](https://github.com/data-engineering-helpers/mds-in-a-box/tree/main/unitycatalog-playground/etc/conf/s3.json)
  (that configuration file is copied into the Docker `s3` container and is used
  to configure the S3 service powered by SeaweedFS)

### Start the Lakehouse

* Start the containers:

```bash
make container-start
```

### Interact with (SeaweedFS-powered) S3

* Browse the [(SeaweedFS) S3-compatible file-system](http://localhost:8888/):

```bash
open http://localhost:8888/
```

* Configure the environment so that it reflects the
  [`etc/conf/s3.json` file](https://github.com/data-engineering-helpers/mds-in-a-box/tree/main/unitycatalog-playground/etc/conf/s3.json):

```bash
export AWS_ACCESS_KEY_ID=1234567890DEMO0KEY00
export AWS_SECRET_ACCESS_KEY=RediDemoKey0011223344556677ToBeReplaced0
export S3_ENDPOINT=http://localhost:8333
export AWS_REGION=us-east-1
```

* With the AWS CLI, list the users:

```bash
aws iam list-users
```

* With the AWS CLI, create the `lakehouse` bucket:

```bash
make init-s3
```

* Note: with SeadweedFS, it does not seem to be possible to create a IAM role.
  The following command is given here for reference only (for now):

```bash
aws iam create-role \
  --role-name arn:aws:iam::987654321:role/UCDbRole-EXAMPLE \
  --assume-role-policy-document etc/conf/iam-uc-master.json
```

### Interact with Unity Catalog (UC)

* For each of the following actions, two versions are given, one with the
  UC CLI, the other one with the UC REST API

* List the catalogs:

```bash
uc catalog list
curl "http://localhost:8080/api/2.1/unity-catalog/catalogs"
```

* List the schemas:

```bash
uc schema list --catalog unity
curl "http://localhost:8080/api/2.1/unity-catalog/schemas?catalog_name=unity"
```

* List the tables:

```bash
uc table list --catalog unity --schema default
curl "http://localhost:8080/api/2.1/unity-catalog/tables?catalog_name=unity&schema_name=default"
```

* Get the details of a given table:

```bash
uc table get --full_name unity.default.marksheet
curl "http://localhost:8080/api/2.1/unity-catalog/tables/unity.default.marksheet"
```

* Browse the first few records of a given table. `uc table read` uses the
  vended creds, which include the stub `s3.sessionToken.0`; SeaweedFS won't
  recognize that token, so the Homebrew `uc` reaching S3 directly will be
  rejected with `InvalidAccessKeyId`. For a managed Delta table on SeaweedFS
  that reads end-to-end, use the in-container `*-sw` targets described in
  [Managed Delta tables on SeaweedFS (sw)](#managed-delta-tables-on-seaweedfs-sw):

```bash
uc table read --full_name unity.default.marksheet --max_results 5
```

* See also
  [GitHub - UC - CLI usage](https://github.com/unitycatalog/unitycatalog/blob/main/docs/usage/cli.md)
  on how to create and use credentials and external locations for Unity Catalog

* Create a credential (for the external location to be created below):

```bash
uc credential create --name lh_aws_cred \
   --aws_iam_role_arn arn:aws:iam::987654321:role/UCDbRole-EXAMPLE
```

* Get the details of the just-created credential:

```bash
uc credential get --name lh_aws_cred
```

* Create an external location on S3:

```bash
uc external_location create --name lh_ext_loc \
   --url s3://lakehouse/unitycatalog/storage \
   --credential_name lh_aws_cred
```

* Get the details of the just-created external location:

```bash
uc external_location get --name lh_ext_loc
```

* Create the `unityxt` extended (xt) catalog and Bronze schema:

```bash
make init-uc-cat-sch
```

* Create a table managed by the `unityxt` extended (xt) catalog. UC needs
  the schema-level `--storage_root` (set by `init-uc-cat-sch`) to allocate
  the staging table on S3 instead of `file:///tmp/`:

```bash
make init-uc-table
```

#### Managed Delta tables on SeaweedFS (sw)

* The `*-sw` targets create a `unitysw` catalog and `bronze` schema whose
  storage root is the SeaweedFS bucket (`s3://lakehouse/warehouse`), then create
  and read a `dim_customer` managed Delta table on it:

```bash
make init-s3              # create the lakehouse bucket (host AWS CLI -> :8333)
make init-uc-cat-sch-sw   # catalog + schema with s3://lakehouse/warehouse root
make init-uc-table-sw     # create the dim_customer managed Delta table
make list-tables-sw
make read-table-dim_customer
```

* Unlike the other targets, the `*-sw` targets run the `uc` CLI **inside the
  `unity-catalog` container** (`docker exec ... ./bin/uc`) rather than the
  Homebrew `uc` on the host. This is required because creating a managed Delta
  table writes the Delta log directly to `s3a://` through Hadoop S3A from the
  CLI, and:

  1. The Homebrew/upstream CLI cannot point Hadoop S3A at a non-AWS endpoint, so
     it always reaches real AWS and fails with
     `Creating directories ... s3GetFileStatus` (see
     [issue #2](https://github.com/data-engineering-helpers/mds-in-a-box/issues/2)).
     The `infrahelpers/unitycatalog` image carries the fork's S3A endpoint fix
     and honors `AWS_ENDPOINT_URL`, which the Makefile sets to
     `http://host.docker.internal:8333`.

  2. UC vends a placeholder session token (`s3.sessionToken.0` in
     `etc/conf/server.properties`) that SeaweedFS rejects with
     `InvalidAccessKeyId`. The mounted
     [`etc/conf/core-site.xml`](./etc/conf/core-site.xml) forces Hadoop S3A to
     use `SimpleAWSCredentialsProvider`, signing with the static access key and
     secret only (no token), which SeaweedFS accepts.

### Stop the Lakehouse

* At the end of the session, stop the containers:

```bash
make container-stop
```

## Setup

### Docker ecosystem

* Download the package installer corresponding to the platform
  on the [Rancher Desktop site](https://rancherdesktop.io/)

* Install a few Docker plugins, on MacOS:

```bash
brew install docker-compose
brew install docker-buildx
```

### Unity Catalog client

* As the Unity Catalog (UC) server is powered by a dedicated container launched
  by Docker Compose, installing UC also brings the client, namely the `uc` CLI
  utility

* Install Unity Catalog (UC) on MacOS:

```bash
brew install unitycatalog
uc --version
```

### AWS CLI

* Even though the S3 service is powered by SeaweedFS, the CLI tool is still
  the one from AWS

* Install the AWS CLI on MacOS:

```bash
brew install awscli
```

# Knowledge Sharing (KS) - Spark - SCD2 with Delta

## Table of Content (ToC)

* [Knowledge Sharing (KS) \- Spark \- SCD2 with Delta](#knowledge-sharing-ks---spark---scd2-with-delta)
  * [Table of Content (ToC)](#table-of-content-toc)
  * [Overview](#overview)
  * [Getting started](#getting-started)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)

## Overview

This
[directory](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/data-processing/spark/examples/000-data-setup/)
allows to manage (_i.e._, create/generate, delete/clean) sample datasets for
[Spark-related tutorials/examples](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/data-processing/spark/examples/README.md)
themselves featured in the
[Spark-related cheat sheets](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/data-processing/spark/README.md).

Some of the Spark-related tutorials require the sample datasets managed in
this directory.

## Getting started

* Clean any previous work (including local Spark warehouse/database,
  Python virtual environment):

```bash
make cleaners
```

* Initialize the uv virtual environment (_e.g._, uv installs the Python dependencies
  in that dedicated virtual environment):

```bash
make init update
```

* Generate the sample snapshots and delta data-sets (it creates Parquet files
  for `init`, `full1`, `full2`, `delta1`, and `delta2`, partitioned by
  `extraction_date`):

```bash
make init-datasets
```

* Analyze the generated data-sets with Datanomy:

```bash
make check-dataset-init
make check-dataset-full1
make check-dataset-full2
make check-dataset-delta1
make check-dataset-delta2
```

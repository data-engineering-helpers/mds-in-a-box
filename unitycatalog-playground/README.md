# Modern Data Stack (MDS) in a box

## Table of Content (ToC)

## Overview

[This section](https://github.com/data-engineering-helpers/mds-in-a-box/tree/main/unitycatalog-playground/)
is part of the
[Modern Data Stack (MDS) in a box Knowledge Sharing (KS) repository](https://github.com/data-engineering-helpers/mds-in-a-box)
and showcases the open source Unity Catalog project and introduces a full
notebook environment for simplifying how to work with the open source (OSS)
version of Unity Catalog (UC).

## References

* [Material for the Data platform - Modern Data Stack (MDS) in a box](https://github.com/data-engineering-helpers/mds-in-a-box)
* [GitHub - Unity Catalog playground](https://github.com/newfront/unitycatalog-playground)
* [GitHub - Lakehouse at home](https://github.com/lisancao/lakehouse-at-home)
* Author: Lisa N. Cao
  ([Lisa N. Cao on LinkedIn](https://www.linkedin.com/in/lisancao/),
  [Lisa N. Cao on GitHub](https://github.com/lisancao))
* [Medium - Declarative Pipelining in Apache Spark Part 1](https://medium.com/apache-spark/declarative-pipelining-in-apache-spark-part-1-focus-on-your-data-not-your-dags-553a1056d178),
  March 2026

### Docker

* [Rancher Desktop](https://rancherdesktop.io/)
  * [GitHub - Rancher Desktop](https://github.com/rancher-sandbox/rancher-desktop/)
  * [Rancher Desktop doc - Install on Linux](https://docs.rancherdesktop.io/getting-started/installation/#linux)
* [Docker doc - Getting Started](https://www.docker.com/get-started/)
  * [Docker doc - Install Docker Compose on Linux](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually)

## Getting Started

* Start the containers:

```bash
make container-start
```

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

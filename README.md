# nwpc-hpc-exporter

[![Build Status](https://travis-ci.org/perillaroc/nwpc-hpc-exporter.svg?branch=master)](https://travis-ci.org/perillaroc/nwpc-hpc-exporter)

A Prometheus exporter for HPC metrics using in NWPC.

## Features

- disk space
- disk usage
- LoadLeveler class
- Slurm partition

## Installation

```bash
pip install .
```

## Configure

See configure sample files in `nwpc_hpc_exporter/xxx/conf` directory.

## Usage

Use installed commands to run exporters. Such as:

```bash
disk_space --config-file='some config file path'
```

## Use Docker

Get Docker image from Docker Hub. Run a container with port and volume mapped.

```bash
docker pull perillaroc/nwpc-hpc-exporter:disk-space

docker run -d -p 8101:8101 -v /some_path/disk_space.config.yml:/etc/nwpc-hpc-exporter/disk_space.config.yml \
    perillaroc/nwpc-hpc-exporter:disk-space
```

### Build docker image

First, build the base image nwpc-hpc-exporter.

```bash
docker build -t perillaroc/nwpc-hpc-exporter -f ./docker/nwpc_hpc_exporter/Dockerfile .
```

Then, build other exporter images. Such as disk space exporter.

```bash
docker build -t perillaroc/nwpc-disk-space-exporter -f ./docker/disk_space/Dockerfile .
```

Finally, run a docker container with port and volume mapped.

```bash
docker run -d -p 8101:8101 -v /some_path/disk_usage.config.yml:/etc/nwpc-hpc-exporter/disk_usage.config.yml \
    perillaroc/nwpc-disk-usage-exporter
```

## LICENSE

Copyright &copy; 2017-2019, Perilla Roc.

`nwpc-hpc-exporter` is licensed under [GPL v3.0](LICENSE.md)
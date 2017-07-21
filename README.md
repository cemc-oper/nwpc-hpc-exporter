# nwpc-hpc-exporter

A Prometheus exporter for HPC metrics using in NWPC.

## Features

- disk space
- disk usage
- loadleveler class

## Installation

```bash
python setup.py install
```

## Configure

See configure sample files in `conf` directory.

## Usage

Use installed commands to run exporters. Such as:

```bash
disk_space --config-file='some config file path'
```

## Using Docker

First, build the base image nwpc-hpc-exporter.

```bash
cd ./docker/nwpc_hpc_exporter
docker build -t perillaroc/nwpc-hpc-exporter .
```

Then, build other exporter images. Such as disk space exporter.

```bash
cd ./docker/disk_space
docker build -t perillaroc/nwpc-disk-space-exporter .
```

Finally, run a docker container with port volume mapped.

```bash
docker run -d -p 8101:8101 -v ./dist/conf:/etc/nwpc-hpc-exporter \
    perillaroc/nwpc-disk-usage-exporter
```

## LICENSE

GPL v3.0
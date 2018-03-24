FROM perillaroc/nwpc-hpc-exporter:latest

LABEL maintainer="perillaroc@gmail.com"

EXPOSE 8105

ENTRYPOINT ["/usr/local/bin/slurm_partition_exporter"]
CMD ["--config-file=/etc/nwpc-hpc-exporter/slurm_partition.config.yml"]
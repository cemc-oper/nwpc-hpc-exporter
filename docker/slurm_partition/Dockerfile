FROM perillaroc/nwpc-hpc-exporter:latest

LABEL maintainer="perillaroc@gmail.com"

ENV NWPC_SLURM_PARTITION_EXPORTER_CONFIG "/etc/nwpc-hpc-exporter/slurm_partition.config.yml"

EXPOSE 8105

ENTRYPOINT exec /usr/local/bin/slurm_partition_exporter --config-file=${NWPC_SLURM_PARTITION_EXPORTER_CONFIG}
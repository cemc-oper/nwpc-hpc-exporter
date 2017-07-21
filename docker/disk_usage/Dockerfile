FROM perillaroc/nwpc-hpc-exporter:latest

LABEL maintainer="perillaroc@gmail.com"

ENV NWPC_DISK_USAGE_EXPORTER_CONFIG "/etc/nwpc-hpc-exporter/disk_usage.config.yml"

EXPOSE 8102

ENTRYPOINT exec /usr/local/bin/disk_usage_exporter --config-file=${NWPC_DISK_USAGE_EXPORTER_CONFIG}
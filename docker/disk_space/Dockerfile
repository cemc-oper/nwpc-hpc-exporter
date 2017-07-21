FROM perillaroc/nwpc-hpc-exporter:latest

LABEL maintainer="perillaroc@gmail.com"

ENV NWPC_DISK_SPACE_EXPORTER_CONFIG "/etc/nwpc-hpc-exporter/disk_space.config.yml"

EXPOSE 8101

ENTRYPOINT exec /usr/local/bin/disk_space_exporter --config-file=${NWPC_DISK_SPACE_EXPORTER_CONFIG}
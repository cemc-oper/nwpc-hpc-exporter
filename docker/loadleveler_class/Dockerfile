FROM perillaroc/nwpc-hpc-exporter:latest

LABEL maintainer="perillaroc@gmail.com"

ENV NWPC_LOADLEVELER_CLASS_EXPORTER_CONFIG "/etc/nwpc-hpc-exporter/loadleveler_class.config.yml"

EXPOSE 8103

ENTRYPOINT exec /usr/local/bin/loadleveler_class_exporter --config-file=${NWPC_LOADLEVELER_CLASS_EXPORTER_CONFIG}
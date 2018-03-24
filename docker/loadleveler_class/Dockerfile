FROM perillaroc/nwpc-hpc-exporter:latest

LABEL maintainer="perillaroc@gmail.com"

EXPOSE 8103

ENTRYPOINT ["/usr/local/bin/loadleveler_class_exporter"]
CMD ["--config-file=/etc/nwpc-hpc-exporter/loadleveler_class.config.yml"]
FROM perillaroc/nwpc-hpc-exporter:latest

MAINTAINER Perilla Roc <perillaroc@gmail.com>

EXPOSE 8102

ENTRYPOINT [ "/usr/local/bin/disk_usage_exporter" ]

CMD ["--config-file=/etc/nwpc-hpc-exporter/disk_usage.config.yml"]
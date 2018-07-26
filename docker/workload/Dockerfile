FROM perillaroc/nwpc-hpc-exporter:latest

LABEL maintainer="perillaroc@gmail.com"

EXPOSE 8103

ENTRYPOINT ["/usr/local/bin/workload_exporter"]
CMD ["--config-file=/etc/nwpc-hpc-exporter/workload.config.yml"]
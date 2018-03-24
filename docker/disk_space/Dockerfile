FROM perillaroc/nwpc-hpc-exporter:latest

LABEL maintainer="perillaroc@gmail.com"

EXPOSE 8101

ENTRYPOINT ["/usr/local/bin/disk_space_exporter"]
CMD ["--config-file=/etc/nwpc-hpc-exporter/disk_space.config.yml"]
FROM python:3

LABEL maintainer="perillaroc@gmail.com"

VOLUME ["/etc/nwpc-hpc-exporter"]

RUN mkdir -p /nwpc-hpc-exporter && \
    chown -R nobody:nogroup /nwpc-hpc-exporter

COPY nwpc_hpc_exporter/ /nwpc-hpc-exporter/nwpc_hpc_exporter/
COPY vendor/ /nwpc-hpc-exporter/vendor/
COPY README.md /nwpc-hpc-exporter/README.md
COPY setup.py /nwpc-hpc-exporter/setup.py

RUN cd /nwpc-hpc-exporter \
    && pip install -e vendor/nwpc-hpc-model \
    && pip install -e .

WORKDIR "/nwpc-hpc-exporter"

CMD ["python3"]


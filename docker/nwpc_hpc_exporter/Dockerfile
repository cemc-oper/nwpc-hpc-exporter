FROM python:3

LABEL maintainer="perillaroc@gmail.com"

VOLUME ["/etc/nwpc-hpc-exporter"]

RUN git clone https://github.com/perillaroc/nwpc-hpc-exporter.git \
    && pip install -e vendor/npwc-hpc-model \
    && pip install -e .

CMD ["python3"]


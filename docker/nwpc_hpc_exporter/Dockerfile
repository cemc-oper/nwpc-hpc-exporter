FROM python:3

LABEL maintainer="perillaroc@gmail.com"

VOLUME ["/etc/nwpc-hpc-exporter"]

RUN git clone https://github.com/perillaroc/nwpc-hpc-exporter.git \
    && cd nwpc-hpc-exporter/vendor/nwpc-hpc-model \
    && python3 setup.py install \
    && cd ../../ \
    && python3 setup.py install

CMD ["python3"]


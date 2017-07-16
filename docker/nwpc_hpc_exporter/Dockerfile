FROM python:3

MAINTAINER Perilla Roc <perillaroc@gmail.com>

RUN git clone https://github.com/perillaroc/nwpc-hpc-exporter.git \
    && cd nwpc-hpc-exporter/vendor/nwpc-hpc-model \
    && python3 setup.py install \
    && cd ../../ \
    && python3 setup.py install

CMD ["python3"]


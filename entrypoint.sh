#!/bin/sh
RUN wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz
RUN gunzip enwiki-latest-abstract.xml.gz
cd /opt/etl/datasets
mkdir wiki
cd ..
mv enwiki-latest-abstract.xml /opt/etl/datasets/wiki/
export PYSPARK_DRIVER_PYTHON=$(which python3)
export PYTHON_VERSION=$(which python3)
make run
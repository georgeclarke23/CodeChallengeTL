FROM ubuntu:latest

# Install OpenJDK 8
RUN \
  apt-get update && \
  apt-get install -y openjdk-8-jdk && \
  rm -rf /var/lib/apt/lists/*

# Install Python
RUN \
    apt-get update && \
    apt-get install -y python3 python3-dev python3-pip python3-virtualenv && \
    rm -rf /var/lib/apt/lists/*

# Install PySpark and Numpy
RUN pip3 install pyspark

RUN apt-get update && apt-get install wget make sudo -y

RUN mkdir -p /opt/etl/app

COPY requirements.txt /opt/etl/

# Install python packages
RUN pip3 install -r /opt/etl/requirements.txt

WORKDIR /opt/etl

COPY Makefile /opt/etl/
COPY app /opt/etl/app/
COPY main.py /opt/etl/
COPY entrypoint.sh /opt/etl/
RUN chmod +x /opt/etl/entrypoint.sh
COPY .env /opt/etl/

RUN mkdir -p /opt/etl/datasets/movies
COPY datasets/movies /opt/etl/datasets/movies

RUN mkdir -p /opt/etl/jars
COPY jars /opt/etl/jars

ENTRYPOINT ["/opt/etl/entrypoint.sh"]

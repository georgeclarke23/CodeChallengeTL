FROM amazonlinux:2

# Linux Dependencies
RUN yum install postgresql java-1.8.0-openjdk python3 python3-pip wget gnuzip build-essential which make -y

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

RUN mkdir -p /opt/etl/app

COPY requirements.txt /opt/etl/

# Install python packages
RUN python3 -m pip install -r /opt/etl/requirements.txt

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

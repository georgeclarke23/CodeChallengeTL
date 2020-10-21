FROM masroorhasan/pyspark

RUN apt-get install -y \
      apt-transport-https \
      ca-certificates \
      curl \
      make \
      unzip \
      software-properties-common

RUN mkdir -p /opt/etl/app

COPY requirements.txt /opt/etl/

# Install python packages
RUN pip install -r /opt/etl/requirements.txt

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

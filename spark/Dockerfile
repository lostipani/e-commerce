FROM python:3.12-bullseye as spark-base
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sudo \
    curl \
    vim \
    unzip \
    rsync \
    openjdk-11-jdk \
    build-essential \
    software-properties-common \
    ssh \
    iproute2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*do

# set python env
COPY spark/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# set env variables
ARG SPARK_VERSION=3.5.5
ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"} \
    HADOOP_HOME=${HADOOP_HOME:-"/opt/hadoop"} \
    JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/ \
    PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}" \
    SPARK_MASTER="spark://spark-master:7077" \
    SPARK_MASTER_HOST=spark-master \
    SPARK_MASTER_PORT=7077 \
    SPARK_NO_DAEMONIZE=true \
    PYSPARK_PYTHON=python3 \
    PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

# download and install Spark
RUN mkdir -p ${HADOOP_HOME} ${SPARK_HOME}
WORKDIR ${SPARK_HOME}
RUN wget https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz \
    && tar xvzf spark-$SPARK_VERSION-bin-hadoop3.tgz --directory /opt/spark \
    --strip-components 1 && rm -rf spark-$SPARK_VERSION-bin-hadoop3.tgz

# set up Spark
FROM spark-base as pyspark
COPY spark/spark-defaults.conf "$SPARK_HOME/conf"
RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*

# set up jupyter notebook
RUN mkdir -p /app/data /app/notebooks

# set up the entrypoint
COPY spark/entrypoint.sh .
RUN chmod 777 ./entrypoint.sh

EXPOSE 7077 8080 8888

# run as non root
# this is in conflict with mounting local folders with different ownership
# uncomment to enable:
# RUN useradd -m -s /bin/bash spark && \
#     chown -R spark:spark /opt/spark /app /opt/hadoop
# USER spark

ENTRYPOINT ["./entrypoint.sh"]

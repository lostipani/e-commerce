FROM my-spark:3.5.5 AS spark-source
FROM apache/airflow:3.1.8-python3.12

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=spark-source /opt/spark /opt/spark
COPY --from=spark-source /opt/hadoop /opt/hadoop

ENV SPARK_HOME=/opt/spark \
    HADOOP_HOME=/opt/hadoop \
    JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 \
    SPARK_MASTER="spark://spark-master:7077" \
    SPARK_MASTER_HOST=spark-master \
    SPARK_MASTER_PORT=7077 \
    PYSPARK_PYTHON=python3 \
    PATH="/opt/spark/bin:/opt/spark/sbin:${PATH}"

ENV PYTHONPATH="${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-0.10.9.7-src.zip"

RUN chmod u+x ${SPARK_HOME}/bin/* ${SPARK_HOME}/sbin/*

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
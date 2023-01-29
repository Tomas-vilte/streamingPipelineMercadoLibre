FROM apache/airflow:2.5.0
COPY /requirements.txt /requirements.txt

RUN pip install kafka-python
RUN pip install apache-airflow-providers-apache-spark
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt
USER root

# Install OpenJDK-11
RUN apt update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME
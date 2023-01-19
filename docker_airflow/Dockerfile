FROM apache/airflow:2.5.0
COPY /requirements.txt /requirements.txt
## RUN pip install kafka-python
RUN pip install airflow-provider-kafka
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt
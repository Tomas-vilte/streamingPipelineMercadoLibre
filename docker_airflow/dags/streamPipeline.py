from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from mongoStatus import statusMongo
from airflow.models.baseoperator import chain
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from producerKafka import runKafkaProducer


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
        dag_id='Streaming_pipeline_meli',
        default_args=default_args,
        description='Ejeccucion del pipeline',
        start_date=datetime(2023, 1, 17),
        schedule=None,
        catchup=False
) as dag:
    consumerRunning = EmptyOperator(
        task_id='Starting_consumer_task',
        dag=dag
    )

    sparkConsumer = SparkSubmitOperator(
        task_id='consumer_data_of_topic',
        packages='org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1',
        application='/opt/airflow/dags/consumerSpark.py',
        #application='/home/tomi/streamingPipelineMercadoLibre/docker_airflow/dags/consumerSpark.py',
        dag=dag
    )
    producerRunning = BashOperator(
        task_id='Running_producer',
        dag=dag,
        bash_command='sleep 30'
    )

    producerTask = PythonOperator(
            task_id='Submit_data_to_kafka',
            python_callable=runKafkaProducer,
            dag=dag
    )

    mongoInfo = PythonOperator(
        task_id="Status_info_mongodb",
        python_callable=statusMongo,
        dag=dag
    )

chain(
    consumerRunning,
    mongoInfo,
    sparkConsumer
)

chain(producerRunning,
      producerTask)


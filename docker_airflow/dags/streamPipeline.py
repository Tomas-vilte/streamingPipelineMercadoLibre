from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from mongoStatus import statusMongo
from airflow.models.baseoperator import chain
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from producerKafka import runKafkaProducer
from postgresStatus import statusPostgres
from loadDataToRds import uploadData


default_args = {
    'owner': 'airflow', # Dueño del pipeline
    'depends_on_past': False, # Establecer en false para ejecutar la canalización incluso si las tareas anteriores fallaron
    'email_on_failure': False, # El correo electrónico no se enviará por fallas en el pipeline
    'email_on_retry': False, # No se enviará correo electrónico para reintentos del pipeline
    'retries': 5, # Número de veces que se volverá a ejecutar el pipeline en caso de falla
    'retry_delay': timedelta(minutes=5) # Intervalo de tiempo entre reintentos
}

with DAG(
        dag_id='Streaming_pipeline_meli',
        default_args=default_args,
        description='Ejeccucion del pipeline',
        start_date=datetime(2023, 1, 17),
        schedule=None,
        catchup=False
) as dag:

    # Tarea 1: ejecutar un operador vacío para iniciar la canalización
    consumerRunning = EmptyOperator(
        task_id='Starting_consumer_task',
        dag=dag
    )
    # Tarea 2: Ejecutar los datos del consumidor usando SparkSubmitOperator
    sparkConsumer = SparkSubmitOperator(
        task_id='consumer_data_of_topic',
        packages='org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1',
        application='/opt/airflow/dags/consumerSpark.py',
        #application='/home/tomi/streamingPipelineMercadoLibre/docker_airflow/dags/consumerSpark.py',
        dag=dag
    )
    # Tarea 3: Ejecutar un operador bash para esperar 30 segundos antes de ejecutar el productor
    producerRunning = BashOperator(
        task_id='Running_producer',
        dag=dag,
        bash_command='sleep 60'
    )
    # Tarea 4: envío de datos al tema de Kafka mediante una función de python
    producerTask = PythonOperator(
            task_id='Submit_data_to_kafka',
            python_callable=runKafkaProducer,
            dag=dag
    )
    # Tarea 5: Obtener el estado de la base de datos MongoDB
    mongoInfo = PythonOperator(
        task_id="Status_info_mongodb",
        python_callable=statusMongo,
        dag=dag
    )
    # Tarea 6: Iniciar la carga de datos a AWS RDS
    startingCharge = EmptyOperator(
        task_id="Starting_upload_to_postgres",
        dag=dag
    )
    # Tarea 7: Obtener estado de la base de datos Postgres
    postgresInfo = PythonOperator(
        task_id='Status_info_postgres',
        python_callable=statusPostgres,
        op_kwargs={
            'host': 'mydatabase.cnfp6axcdse9.us-east-1.rds.amazonaws.com',
            'port': 5432,
            'database': 'meliAnalytics',
            'user': 'postgres',
            'password': 'postgres'
        },
        dag=dag
    )
    # Tarea 8: Subir los datos recolectados de MongoDB a Postgres
    loadDataToAws = PythonOperator(
        task_id='Uploading_data_to_aws_rds',
        dag=dag,
        python_callable=uploadData
    )
    # Tarea 9: Inicializa el stream pipeline
    initStreamingPipeline = EmptyOperator(
        task_id="Initialize_streaming_pipeline",
        dag=dag
    )
    # Tarea 10: Inicializa las tareas
    initTasks = EmptyOperator(
        task_id="Initialize_the_tasks",
        dag=dag
    )

chain(initTasks, initStreamingPipeline, [producerRunning, consumerRunning], [producerTask, sparkConsumer],
      startingCharge, [mongoInfo, postgresInfo], loadDataToAws)

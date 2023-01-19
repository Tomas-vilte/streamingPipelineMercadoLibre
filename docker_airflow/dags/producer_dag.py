import json
from datetime import timedelta, datetime
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from kafka import KafkaProducer
from loggin import log


def runKafkaProducer():
    try:
        producer = KafkaProducer(bootstrap_servers='172.17.0.1:9092',
                                 value_serializer=lambda x:
                                 json.dumps(x).encode('utf-8'))
        log.info(f'Conexion exitosa a kafka: {producer}')
    except Exception as e:
        log.error(f'Hubo un error al conectarse a kafka: {e}')
    # Hace la solicitud HTTP a la API de Meli para obtener el número total de resultados
    api_url = 'https://api.mercadolibre.com/sites/MLA/search?category=MLA3794'
    response = requests.get(api_url)

    # Inicializa un contador de resultados
    results_count = 0

    # Crea un bucle while para verificar si se ha agregado un nuevo producto
    while True:
        # Hace la solicitud HTTP a la API de Meli
        api_url = f'https://api.mercadolibre.com/sites/MLA/search?category=MLA3794&offset={results_count}'

        # Obtiene los resultados de la respuesta JSON
        results = response.json()["results"]

        # Recorre cada resultado y lo envía al tópico de Kafka
        for item in results:
            data = {
                "id": item["id"],
                "nameOfProduct": item["title"],
                "price": item["price"],
                "ProductStatus": item["condition"],
                "SellerName": item["seller"]["nickname"],
                "RegistrationDate": item["seller"]["registration_date"],
                "QuantitySold": item["sold_quantity"],
                "QuantityAvailable": item["available_quantity"],
            }
            producer.send('myTopic', data)
            print(data)

        # Incrementa el contador de resultados en la cantidad de resultados obtenidos
        results_count += len(results)

        # Si se han obtenido todos los resultados, sale del bucle
        if results_count >= 50:
            break

    # Cierra el productor de Kafka
    producer.close()
    log.info(f'Producer cerrado: {producer}')


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
        dag_id='Kafka_consumer',
        default_args=default_args,
        description='Ejeccucion de producer',
        start_date=datetime(2023, 1, 17),
        schedule=None,
        catchup=False
) as dag:
    task = EmptyOperator(
        task_id='starting_task',
        dag=dag
    )

    producer_task = PythonOperator(
        task_id='submit_data_to_kafka',
        python_callable=runKafkaProducer,
        dag=dag
    )

task >> producer_task

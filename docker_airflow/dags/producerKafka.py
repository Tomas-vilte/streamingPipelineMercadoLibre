import json
from typing import Any
from loggin import log
import requests
from kafka import KafkaProducer


def runKafkaProducer() -> list[dict[str, Any]]:
    datos = []
    try:
        producer = KafkaProducer(bootstrap_servers=['172.17.0.1:9092'],
                                 value_serializer=lambda x:
                                 json.dumps(x).encode('utf-8'))
        log.info(f'Conexion exitosa a kafka: {producer}')
    except Exception as e:
        log.error(f'Hubo un error al conectarse a kafka: {e}')
    # Hace la solicitud HTTP a la API de Meli para obtener el número total de resultados
    api_url = 'https://api.mercadolibre.com/sites/MLA/search?category=MLA3794'
    response = requests.get(api_url)

    # Verifica si la respuesta es un código de estado 200
    if response.status_code != 200:
        log.error(f'La URL de la api es inválida: {response.status_code}')
        raise Exception('La url de la api es invalida')
    # Inicializa un contador de resultados
    results_count = 0
    api_count = f'https://api.mercadolibre.com/sites/MLA/search?category=MLA3794&offset={results_count}'

    # Crea un bucle while para verificar si se ha agregado un nuevo producto
    while True:
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
            datos.append(data)
            producer.send('myTopic', datos)
            print(datos)
        # Incrementa el contador de resultados en la cantidad de resultados obtenidos
        results_count += len(results)

        # Si se han obtenido todos los resultados, sale del bucle
        if results_count >= 50:
            break

    # Cierra el productor de Kafka
        producer.close()
        log.info(f'Producer cerrado: {producer}')

    return datos

if __name__ == '__main__':
    runKafkaProducer()
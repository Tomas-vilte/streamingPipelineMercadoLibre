import requests
from kafka import KafkaProducer
import json


def runKafkaProducer():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))

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


if __name__ == '__main__':
    runKafkaProducer()

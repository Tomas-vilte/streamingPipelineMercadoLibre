import json
from unittest.mock import patch, MagicMock
import unittest
import requests

from producerKafka import runKafkaProducer
from kafka import KafkaProducer

# Definimos una clase que hereda de unittest.TestCase
class TestRunKafkaProducer(unittest.TestCase):

    # Definimos un método de prueba para verificar la conexión con el servidor Kafka
    def test_connection(self):
        # Creamos una instancia de la clase KafkaProducer
        producer = KafkaProducer(bootstrap_servers=['172.17.0.1:9092'],
                                 value_serializer=lambda x:
                                 json.dumps(x).encode('utf-8'))
        # Verificamos que la instancia de KafkaProducer no sea None
        self.assertIsNotNone(producer)

    # Definimos un método de prueba para verificar los datos devueltos por runKafkaProducer
    def test_data(self):
        # Llamamos al método runKafkaProducer
        datos = runKafkaProducer()
        # Verificamos que los datos devueltos por runKafkaProducer sean una lista
        self.assertIsInstance(datos, list)
        # Verificamos que la lista tenga al menos un elemento
        self.assertGreater(len(datos), 0)
        # Verificamos que cada elemento de la lista sea un diccionario
        for item in datos:
            # Verificamos que el elemento es un diccionario
            self.assertIsInstance(item, dict)
            # Verificamos que cada diccionario tenga las siguientes claves
            # Verificar que el diccionario contiene una clave 'id'
            self.assertIn('id', item)
            # Verificar que el diccionario contiene una clave 'nameOfProduct'
            self.assertIn('nameOfProduct', item)
            # Verificar que el diccionario contiene una clave 'price'
            self.assertIn('price', item)
            # Verificar que el diccionario contiene una clave 'ProductStatus'
            self.assertIn('ProductStatus', item)
            # Verificar que el diccionario contiene una clave 'SellerName'
            self.assertIn('SellerName', item)
            # Verificar que el diccionario contiene una clave 'RegistrationDate'
            self.assertIn('RegistrationDate', item)
            # Verificar que el diccionario contiene una clave 'QuantitySold'
            self.assertIn('QuantitySold', item)
            # Verificar que el diccionario contiene una clave 'QuantityAvailable'
            self.assertIn('QuantityAvailable', item)

    # Definimos un método de prueba para verificar la respuesta de la API
    @patch('requests.get')
    def test_api_response(self, mock_get):
        # Creamos un objeto mock_response para simular la respuesta de la API
        mock_response = MagicMock()
        # Establecemos el atributo status_code en 200
        mock_response.status_code = 200
        # Establecemos la respuesta del método json como un diccionario
        mock_response.json.return_value = {'key': 'value'}
        # Asignamos el objeto mock_response a la llamada a mock_get
        mock_get.return_value = mock_response

        # Definimos la url de la api
        api_url = 'https://api.mercadolibre.com/sites/MLA/search?category=MLA3794'
        # Realizamos una petición get a la api
        response = requests.get(api_url)

        # Verificamos que el código de respuesta sea 200
        self.assertEqual(response.status_code, 200)

        # Verificamos que la respuesta de la API sea un diccionario
        self.assertIsInstance(response.json(), dict)
        # Verificamos que mock_get sea llamado con la url de la api
        mock_get.assert_called_with(api_url)

    def test_producer_close(self):
        """
        Prueba para verificar que el productor se haya cerrado correctamente
        """
        # Creamos una instancia de la clase KafkaProducer
        producer = KafkaProducer(bootstrap_servers=['172.17.0.1:9092'],
                                 value_serializer=lambda x:
                                 json.dumps(x).encode('utf-8'))
        # Verificamos que el producer de kafka se cerro correctamente
        producer.close()
        self.assertTrue(producer.close)


if __name__ == '__main__':
    unittest.main()

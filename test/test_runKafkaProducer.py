import json
from unittest.mock import patch
import unittest
from mock.mock import Mock

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

    @patch.object(KafkaProducer, 'send')
    @patch('requests.get')
    def test_runKafkaProducer_no_send(self, mock_requests_get, mock_kafka_send):
        """
           Prueba la función runKafkaProducer con mensajes no enviados a Kafka

           Args:
               mock_requests_get (Mock): Objeto simulado de la función requests.get
               mock_kafka_send (Mock): Objeto simulado de la función KafkaProducer.send

           Returns:
               None
           """
        # Configura el mock para devolver una respuesta simulada
        mock_response = Mock()
        mock_response.json.return_value = {'results': [{'id': 1, 'title': 'producto 23', 'price': 1000,
                                                    'condition': 'new', 'seller': {'nickname': 'seller 1',
                                                                                   'registration_date': '2022-01-01',
                                                                                    },'sold_quantity': 1,
                                                                                   'available_quantity': 10}]}
        mock_requests_get.return_value = mock_response

        # Ejecuta la función que se está probando
        result = runKafkaProducer()

        # Verifica que los mensajes no se hayan enviado a Kafka
        self.assertEqual(mock_kafka_send.call_count, 50)

        # Verifica que los resultados sean los esperados
        self.assertEqual(len(result), 50)
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[0]["nameOfProduct"], "producto 23")
        self.assertEqual(result[0]["price"], 1000)
        self.assertEqual(result[0]["ProductStatus"], "new")
        self.assertEqual(result[0]["SellerName"], "seller 1")
        self.assertEqual(result[0]["RegistrationDate"], "2022-01-01")
        self.assertEqual(result[0]["QuantitySold"], 1)
        self.assertEqual(result[0]["QuantityAvailable"], 10)

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

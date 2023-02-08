import unittest
from pyspark.sql import SparkSession
import logging

# Clase de prueba para el código
class TestCode(unittest.TestCase):
    # Configurar log
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Configurar tópico de Kafka y servidores de inicio
    kafka_topic_name = "myTopic"
    kakfa_bootstrap_servers = "172.17.0.1:9092"

    # Inicialización de SparkSession para cada prueba
    def setUp(self):
        self.spark = SparkSession \
            .builder \
            .master("local[*]") \
            .config("spark.mongodb.input.uri", "mongodb://root:secret@172.20.0.8:27017/mercadolibredb.meliproduct") \
            .config("spark.mongodb.output.uri", "mongodb://root:secret@172.20.0.8:27017/mercadolibredb.meliproduct") \
            .config('spark.jars.packages', "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
            .getOrCreate()

    # Cerrar la sesión de Spark después de cada prueba
    def tearDown(self):
        self.spark.stop()

    # Prueba para verificar si SparkSession se crea correctamente
    def test_spark_session(self):
        self.assertIsNotNone(self.spark)

    # Prueba para verificar si el DataFrame se crea correctamente
    def test_dataframe_creation(self):
        # Crear DataFrame de transmisión leyendo mensajes de Kafka
        streamingDF = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kakfa_bootstrap_servers) \
            .option("subscribe", self.kafka_topic_name) \
            .load()

        self.assertIsNotNone(streamingDF)

# Ejecutar las pruebas
if __name__ == '__main__':
    unittest.main()

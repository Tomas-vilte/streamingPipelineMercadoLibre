from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import logging

# Configurar log
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Configurar tópico de Kafka y servidores de inicio
kafka_topic_name = "myTopic"
kakfa_bootstrap_servers = "localhost:9092"


def writeToMongo(df, bacthId):
    """
       La función writeToMongo toma un DataFrame de Spark y una identificación de lote como argumentos y escribe el DataFrame a MongoDB.
    """
    try:
        df.write \
            .format("mongo") \
            .option("uri", "mongodb://127.0.0.1:27017") \
            .option("database", "mercadolibreDB") \
            .option("collection", "meliProduct") \
            .mode("append") \
            .save()
    except Exception as e:
        logger.error(f'Error al escribir en Mongo: {e}')


# Crear sesión de Spark
spark = SparkSession \
    .builder \
    .master("local[*]") \
    .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/mercadolibreDB.meliProduct") \
    .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/mercadolibreDB.meliProduct") \
    .getOrCreate()

# Configurar nivel de registro para mostrar solo errores
spark.sparkContext.setLogLevel("ERROR")

# Crear DataFrame de transmisión leyendo mensajes de Kafka
streamingDF = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kakfa_bootstrap_servers) \
    .option("subscribe", kafka_topic_name) \
    .load()

# Crear DataFrame de cadena seleccionando solo el valor de cada mensaje de Kafka y convirtiéndolo a una cadena
stringDF = streamingDF.selectExpr("CAST(value AS STRING)")

# Crear esquema para el DataFrame
schema = "id STRING," \
         "nameOfProduct STRING," \
         "price FLOAT," \
         "ProductStatus STRING," \
         "SellerName STRING," \
         "RegistrationDate TIMESTAMP," \
         "QuantitySold INTEGER," \
         "QuantityAvailable INTEGER"

# Analiza valores a csv
csvDF = stringDF.select(from_json(col("value"), schema).alias("data"))

# Extrae columnas del csv
schemaDF = csvDF.select("data.*")

# Agrega nueva columna a DataFrame

# Asigna una puntuación basada en el precio y en la cantidad vendida
ratings = when(
    (schemaDF.price > 10000) & (schemaDF.QuantitySold > 500), 5.0
).when(
    (schemaDF.price > 5000) & (schemaDF.QuantitySold <= 500), 4.5
).when(
    (schemaDF.price >= 8500) & (schemaDF.QuantitySold > 50), 4.0
).when(
    (schemaDF.price >= 1000) & (schemaDF.QuantitySold <= 250), 3.5
).otherwise(3.0)

finalDF = schemaDF.filter(schemaDF.RegistrationDate > "2010").withColumn("Free shipping?",
                                                                         when((schemaDF.price >= 25000),
                                                                              lit("Your shipment arrives today")) \
                                                                         .when((schemaDF.price >= 15000) & \
                                                                               (schemaDF.price < 25000),
                                                                               lit("Your shipment arrives tomorrow"))
                                                                         .when((schemaDF.price >= 5000) & \
                                                                               (schemaDF.price <= 3500),
                                                                               lit("It arrives in a few days")) \
                                                                         .otherwise(
                                                                             lit("You have to pay the shipping"))) \
    .withColumn("Store ratings", ratings)

# Escribir los objetos JSON en MongoDB como un flujo
query = finalDF \
    .writeStream \
    .trigger(processingTime='5 seconds') \
    .outputMode("update") \
    .format("console") \
    .start()

# Enviar cada fila del DataFrame de transmisión a la función writeToMongo como RDD
queryToMongo = finalDF.writeStream.foreachBatch(writeToMongo).start()
queryToMongo.awaitTermination()

# Espere a que termine la transmisión
query.awaitTermination()

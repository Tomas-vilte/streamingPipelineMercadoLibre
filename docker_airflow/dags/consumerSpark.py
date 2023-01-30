import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import logging

# Configurar log
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Configurar tópico de Kafka y servidores de inicio
kafka_topic_name = "myTopic"
kakfa_bootstrap_servers = "172.17.0.1:9092"


def writeToMongo(df, bacthId):
    """
       La función writeToMongo toma un DataFrame de Spark y una identificación de lote como argumentos y escribe el DataFrame a MongoDB.
    """
        # Si queres ejecutar esto en airflow en tu local sin usar docker, pero tener mongodb en un contenedor docker,
        # tenes que cambiar las configuraciones de mongo dentro del contenedor dentro del path, /etc/mongod.conf y en la
        # seccion de 'net', donde dice 'bindIp': 127.0.0.1 lo tenes que cambiar a 'bindIp': 172.29.0.2 que es la direccion
        # ip del contendor donde esta mongo, obviamente esta direccion '172.29.0.2' puede ser distinta por lo que tenes
        # que verificar la direccion ip de tu contenedor mongo con este comando
        # docker inspect <container id> | grep "IPAddress"
        # acordate que una vez que modificaste el file mongod.conf tenes que reiniciar el container para que se aplique los cambios
        # !otra cosa importante! es que si vas a usar mongodb en tu local sin usar docker, tenes que cambiar la direccion
        # ip a 127.0.0.1 y te va quedar asi la url: mongodb://127.0.0.1:27017
    try:
        df.write \
            .format("mongo") \
            .option("uri", "mongodb://root:secret@172.20.0.2:27017") \
            .option("database", "mercadolibredb") \
            .option("collection", "meliproduct") \
            .mode("append") \
            .save()
    except Exception as e:
        logger.error(f'Error al escribir en Mongo: {e}')

def stop_stream_query(query, wait_time):
    """
    Detiene una consulta de transmisión en ejecución en Apache Spark.

    Parameters:
    query (spark.sql.streaming.StreamingQuery): La consulta de transmisión a detener.
    wait_time (int): El tiempo de espera para la terminación de la consulta (en segundos).

    Returns:
    None
    """
    # Mientras la consulta esté activa
    while query.isActive:
        msg = query.status['message']
        data_avail = query.status['isDataAvailable']
        trigger_active = query.status['isTriggerActive']
        # Si no hay datos disponibles y el trigger no está activo y el mensaje no es "Inicializando fuentes"
        if not data_avail and not trigger_active and msg != "Initializing sources":
            print('Stopping query...')
            query.stop() # Detener la consulta
        time.sleep(0.5) # Esperar 0.5 segundos

    # Esperar la terminación de la consulta
    print('Awaiting termination...')
    query.awaitTermination(wait_time) # Esperar wait_time segundos para la terminación


# Crear sesión de Spark
spark = SparkSession \
    .builder \
    .master("local[*]") \
    .config("spark.mongodb.input.uri", "mongodb://root:secret@172.20.0.2:27017/mercadolibredb.meliproduct") \
    .config("spark.mongodb.output.uri", "mongodb://root:secret@172.20.0.2:27017/mercadolibredb.meliproduct") \
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

finalDF = schemaDF.withColumn("Free shipping?",
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
    .option("truncate", False) \
    .option("numRows", 50) \
    .outputMode("update") \
    .format("console") \
    .start()

# Enviar cada fila del DataFrame de transmisión a la función writeToMongo como RDD
queryToMongo = finalDF.writeStream.foreachBatch(writeToMongo).start()

# Espere a que termine la transmisión
stop_stream_query(query, 50)
stop_stream_query(queryToMongo, 50)
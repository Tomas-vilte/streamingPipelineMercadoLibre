# streaming_pipeline

## Contenidos
1. [Descripción](#Descripción) 
2. [Requisitos](#Requisitos)
3. [Instalación](#Instalación)
4. [Ejecucción local](#Ejecucciónlocal)
5. [Ejecucción con docker](#Ejecuccióncondocker)
6. [Arquitectura del proyecto](#arquitecturadelproyecto)
7. [Analisis en Google Data Studio](#Analisis)

<a name="Descripción"></a>
## Descripción

Este proyecto es un ejemplo de cómo usar la transmisión de Kafka para leer datos de la API de Mercado Libre, procesarlos y agregar una nueva columna, luego escribir los datos resultantes en una colección de MongoDB. El objetivo principal es obtener datos de productos en tiempo real de MercadoLibre y almacenarlos en MongoDB para su posterior análisis.

<a name="Requisitos"></a>
## Requisitos

- Great Expectations

- Apache Airflow

- Estoy usando Apache Kafka 3.0.0, pero cualquier versión más nueva debería funcionar. Si no sabes como instalarlo podes seguir estas instrucciones de [este](https://kontext.tech/article/1047/install-and-run-kafka-320-on-wsl) tutorial.

- Estoy usando MongoDB 5.0.9, si lo tenes instalado podes seguir estos pasos en este [link](https://docs.mongodb.com/manual/installation/)

- Python 3

- Paquetes de Python requeridos: pyspark, kafka-python, request, json

<a name="Instalación"></a>
## Instalación

Para instalar y utilizar esta aplicación sigue los siguientes pasos:

1. Descarga o clona este repositorio en tu entorno de desarrollo.

2. Cree un entorno virtual e instale los paquetes de Python necesarios con el comando: pip install -r requirements.txt

<a name="Ejecucciónlocal"></a>
## Ejecucción local

1. Antes de proceder a ejecutar nuestro consumidor y productor, debemos verificar si MongoDB se está ejecutando. Primero verificamos su estado, si MongoDB no se está ejecutando, debemos iniciarlo. A continuación se encuentran los comandos para verificar, iniciar y detener MongoDB.
    ```bash
    sudo service mongodb status
    sudo service mongodb start 
    sudo service mongodb stop 
    ```

3. Ejecute los siguientes comandos para iniciar todos los servicios de kafka en el orden correcto:
    ```bash
    # Start the ZooKeeper service
    $ bin/zookeeper-server-start.sh config/zookeeper.properties
    # Start the Kafka broker service
    $ bin/kafka-server-start.sh config/server.properties 
    ```

4. Crear topic para almancenar los eventos:
Entonces, antes de que puedas escribir tus primeros eventos, debes crear un tema. Abra otra sesión de terminal y ejecute:
    ```bash
   $ bin/kafka-topics.sh --create --topic myTopic--bootstrap-server localhost:9092
    ```
5. Leer los eventos: Abra otra sesión de terminal y ejecute el cliente consumidor de la consola para leer los eventos que acaba de crear:
    ```bash
    $ bin/kafka-console-consumer.sh --topic myTopic --from-beginning --bootstrap-server localhost:9092
    ```

6. Ahora que se están ejecutando Kafka y MongoDB, primero comenzaremos a ejecutar el consumidor porque queremos escuchar antes de enviar los datos de transmisión, usaremos el siguiente comando.
      ```bash
      spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 consumer.py
      ```
    Una vez que se envíe la aplicación Spark, veremos cómo está esperando los datos.


    OUTPUT:
    ![](/images/Tabla.png)

7. Ejecutemos al productor ahora. Dado que el productor es solo un script de Python, podemos ejecutarlo como ejecutamos cualquier otro script de Python.
    ```bash
    python3 producer.py
    ```
    El productor comenzará a leer los datos de la api de Mercado Libre y se los enviará al consumidor. El consumidor leerá los datos enviados por el productor y los procesará y almacenará en MongoDB

    OUTPUT:
    ![](/images/output.png)

    Datos almacenados en mongoDB:
    ![](/images/dataMongo.png)


<a name="Ejecuccióncondocker"></a>
## Ejecucción con docker

Si queres ahorrarte tiempo, podes ejecutar el bash script runContainers.sh. Esto solamente levanta todos los contenedores

1. Configure un broker de Kafka:
En la carpeta docker_kafka se encuentra un archivo Docker Compose a continuación ejecutará todo por vos a través de Docker.


2. Inicie el broker de Kafka: Desde el directorio que mencione contiene el docker-compose.yml archivo creado en el paso anterior, ejecute este comando para iniciar todos los servicios en el orden correcto.
    ```bash
    docker compose up -d
    ```
3. Crea un topic: Kafka almacena mensajes en topics. Es una buena práctica crearlos explícitamente antes de usarlos, incluso si Kafka está configurado para crearlos automáticamente cuando se hace referencia a ellos. Ejecute este comando para crear un nuevo topic en el que escribiremos y leeremos algunos mensajes de prueba.
    ```bash
    docker exec broker \
    kafka-topics --bootstrap-server broker:9092 \
             --create \
             --topic myTopic
    ```

4. Escribir mensajes al topic:
    ```bash
    docker exec --interactive --tty broker \
    kafka-console-producer --bootstrap-server broker:9092 \
                       --topic myTopic
    ```

5. Leer mensajes del topic:
    ```bash
    docker exec --interactive --tty broker \
    kafka-console-consumer --bootstrap-server broker:9092 \
                       --topic myTopic \
                       --from-beginning
    ```

6. Detenga el broker de Kafka: Una vez que haya terminado, puede cerrar el broker de Kafka. Tenga en cuenta que hacer esto destruirá todos los mensajes en los temas que ha escrito. Desde el directorio docker_kafka que contiene el docker-compose.yml archivo creado anteriormente, ejecute este comando para detener todos los servicios en el orden correcto.
    ```bash
    docker compose down
    ```

## Docker mongodb

1. En el directorio de docker_mongodb, esta el docker compose. Por lo tanto en una terminal escribi:
    
    ```bash
    docker compose up -d 
    ```

2. Una vez ya levantado el container. Ejecuta este comando para interactuar con el container y asi poder ver los datos en mongoDB:
    ```bash
    docker exet -it my-mongodb bash
    ```
    Una vez ya dentro del container ejecuta estos comandos:
    ```bash
    mongosh mongodb://root:secret@172.22.0.8:27017
    use mercadolibredb
    db.createCollection("meliproduct")
    db.meliproduct.find({})
    ```
    - El primer comando entra a la base de datos de mongoDB
    - El segundo crea una base de datos
    - El tercero crea una coleccion
    - Y el ultimo muestra los resultados

# Docker airflow
1. En el directorio de docker_airflow, esta el docker compose. En una terminal escribi:
    ```bash
    docker compose up -d 
    ```
    Esto iniciara el contenedor y todos los servicios de airflow para que funcione correctamente.

<a name="Analisis"></a>
## Analisis en Google Data Studio:
Para analizar los datos que se recopilan de las tiendas, se utilizará Google Data Studio como plataforma de visualización de datos. Se podrán crear distintos informes para visualizar diferentes métricas, como por ejemplo:

1. Tiendas que más productos vendieron.
2. Tiendas con mejor puntaje en base a los precios y la cantidad vendida.

 ![](/images/Analisis1.png)

3. Tiendas con stock disponible.
4. Tiendas que venden productos a menor precio

![](/images/Analisis2.png)

# Airflow 
El pipeline de procesamiento de datos será gestionado por Apache Airflow, un sistema de orquestación de workflows de código abierto. Airflow permitirá automatizar y monitorear los diferentes procesos que forman parte del pipeline, desde la recopilación de datos hasta su visualización en Google Data Studio.

![](/images/flujo.png)

<a name="arquitecturadelproyecto"></a>
## Arquitectura del proyecto

![](/images/arquitectura.png)

1. Data source: Proveniente de la api de Mercado Libre.

2. Kafka: Kafka se utilizará como herramienta de ingestión para enviar los detalles de los productos a la aplicacion Spark.

3. Spark: Spark será el motor utilizado para procesar los datos en esta canalización de transmisión de datos.

4. Amazon RDS: Se utilizara como data warehouse en una base de datos postgres.

5. Una vez que lo datos se envian al data warehouse pasa por validaciones o test de calidad de datos. para evitar pipeline debt.

6. Por ultimos estos datos son visualizados con la herramienta de Google Data Studio.
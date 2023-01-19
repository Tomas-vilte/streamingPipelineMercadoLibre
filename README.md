# streaming_pipeline

## Contenidos
1. [Descripción](#Descripción) 
2. [Requisitos](#Requisitos)
3. [Instalación](#Instalación)
3. [Uso](#Uso)
4. [Arquitectura del proyecto](#arquitecturadelproyecto)

<a name="Descripción"></a>
## Descripción

Este proyecto es un ejemplo de cómo usar la transmisión de Kafka para leer datos de la API de Mercado Libre, procesarlos y agregar una nueva columna, luego escribir los datos resultantes en una colección de MongoDB. El objetivo principal es obtener datos de productos en tiempo real de MercadoLibre y almacenarlos en MongoDB para su posterior análisis.

<a name="Requisitos"></a>
## Requisitos

- Estoy usando Apache Kafka 3.0.0, pero cualquier versión más nueva debería funcionar. Si no sabes como instalarlo podes seguir estas instrucciones de [este](https://kontext.tech/article/1047/install-and-run-kafka-320-on-wsl) tutorial.

- Estoy usando MongoDB 5.0.9, si lo tenes instalado podes seguir estos pasos en este [link](https://docs.mongodb.com/manual/installation/)

- Python 3

- Paquetes de Python requeridos: pyspark, kafka-python, request, json

<a name="Instalación"></a>
## Instalación

Para instalar y utilizar esta aplicación sigue los siguientes pasos:

1. Descarga o clona este repositorio en tu entorno de desarrollo.

2. Cree un entorno virtual e instale los paquetes de Python necesarios con el comando: pip install -r requirements.txt

<a name="Uso"></a>
## Uso

1. Antes de proceder a ejecutar nuestro consumidor y productor, debemos verificar si MongoDB se está ejecutando. Primero verificamos su estado, si MongoDB no se está ejecutando, debemos iniciarlo. A continuación se encuentran los comandos para verificar, iniciar y detener MongoDB.
    ```bash
    sudo service mongodb status
    sudo service mongodb start 
    sudo service mongodb stop 
    ```

2. Configure un broker de Kafka:
En la carpeta docker_kafka se encuentra un archivo Docker Compose a continuación ejecutará todo por vos a través de Docker.


3. Inicie el broker de Kafka: Desde el directorio que mencione contiene el docker-compose.yml archivo creado en el paso anterior, ejecute este comando para iniciar todos los servicios en el orden correcto.
    ```bash
    docker compose up -d
    ```
4. Crea un topic: Kafka almacena mensajes en topics. Es una buena práctica crearlos explícitamente antes de usarlos, incluso si Kafka está configurado para crearlos automáticamente cuando se hace referencia a ellos. Ejecute este comando para crear un nuevo topic en el que escribiremos y leeremos algunos mensajes de prueba.
    ```bash
    docker exec broker \
    kafka-topics --bootstrap-server broker:9092 \
             --create \
             --topic myTopic
    ```

5. Escribir mensajes al topic:
    ```bash
    docker exec --interactive --tty broker \
    kafka-console-producer --bootstrap-server broker:9092 \
                       --topic myTopic
    ```

6. Leer mensajes del topic:
    ```bash
    docker exec --interactive --tty broker \
    kafka-console-consumer --bootstrap-server broker:9092 \
                       --topic myTopic \
                       --from-beginning
    ```

7. Detenga el broker de Kafka: Una vez que haya terminado, puede cerrar el broker de Kafka. Tenga en cuenta que hacer esto destruirá todos los mensajes en los temas que ha escrito. Desde el directorio docker_kafka que contiene el docker-compose.yml archivo creado anteriormente, ejecute este comando para detener todos los servicios en el orden correcto.
    ```bash
    docker-compose down
    ```

8. Ahora que se están ejecutando Kafka y MongoDB, primero comenzaremos a ejecutar el consumidor porque queremos escuchar antes de enviar los datos de transmisión, usaremos el siguiente comando.
      ```bash
      spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 consumer.py
      ```
    Una vez que se envíe la aplicación Spark, veremos cómo está esperando los datos.


    OUTPUT:
    ![](/images/Tabla.png)

9. Ejecutemos al productor ahora. Dado que el productor es solo un script de Python, podemos ejecutarlo como ejecutamos cualquier otro script de Python.
    ```bash
    python3 productor.py
    ```
    El productor comenzará a leer los datos de la api de Mercado Libre y se los enviará al consumidor. El consumidor leerá los datos enviados por el productor y los procesará y almacenará en MongoDB

    OUTPUT:
    ![](/images/output.png)

    Datos almacenados en mongoDB:
    ![](/images/dataMongo.png)


<a name="arquitectura del proyecto"></a>
## Arquitectura del proyecto
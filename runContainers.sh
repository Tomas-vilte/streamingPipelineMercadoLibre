#!/bin/bash

# Start Docker Compose for Airflow
cd ./docker_airflow
if [ -z "$(docker ps -q -f name=docker_airflow)" ]; then
  docker compose up -d
else
  echo "Airflow contenedores que ya se están ejecutando"
fi

# Start Docker Compose for MongoDB
cd ../docker_mongodb
if [ -z "$(docker ps -q -f name=my-mongodb)" ]; then
  docker compose up -d
else
  echo "MongoDB contenedor que ya se están ejecutando"
fi

# Start Docker Compose for Kafka
cd ../docker_kafka
if [ -z "$(docker ps -q -f name=zookeeper)" ] || [ -z "$(docker ps -q -f name=broker)" ]; then
  docker compose up -d
else
  echo "Kafka contenedor que ya se están ejecutando"
fi

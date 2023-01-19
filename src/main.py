from loadToAws import getDataOfMongo
from posgresClass import DataUploader
from getCredentials import host, port, database, userdb, password

if __name__ == '__main__':
    # Obteniendo los datos de MongoDB
    client = getDataOfMongo(limit=115,database='mercadolibreDB', coleccion='meliProduct')
    # Cargando los datos obtenidos en una base de datos PostgreSQL
    database = DataUploader(host=host, port=port, dbname=database, user=userdb, password=password)
    database.upload_data(client)
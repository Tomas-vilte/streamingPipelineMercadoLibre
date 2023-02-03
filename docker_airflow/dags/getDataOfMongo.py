from pymongo import MongoClient
from src.loggerBase import log


def getDataOfMongo(limit: int, database: str, coleccion: str, host: str = 'mongodb://root:secret@172.20.0.8', port: int = 27017) -> list:
    """
    :param limit: Limite de registros a devolver.
    :param database: Nombre de la base de datos de mongoDB.
    :param coleccion: Nombre de la coleccion.
    :param host: Host.
    :param port: Puerto de la base de datos.
    :return: Esto retorna un diccionario con todos los datos en la coleccion.
    """
    datos = []

    try:
        # Creando una conexión con MongoDB
        clients = MongoClient(host=host, port=port)

        # Obteniendo la base de datos especificada
        db = clients[database]

        # Validamos si la base de datos existe
        if database not in clients.list_database_names():
            log.error(f"La base de datos {database} no existe")
            raise Exception(f"La base de datos {database} no existe")
        else:
            log.info(f'Conexion exitosa a la base de datos: {database}')

        # Obteniendo la colección especificada
        collection = db.get_collection(coleccion)

        # Valida si la collecion existe
        if coleccion not in db.list_collection_names():
            log.error(f"La coleccion {coleccion} no existe en la base de datos {database}")
            raise Exception(f"La coleccion {coleccion} no existe en la base de datos {database}")
        else:
            log.info(f'Obteniendo coleccion: {coleccion}')


        # Obteniendo los registros limitados de la colección
        data = collection
        for document in data.find({}).limit(limit=limit):
            print(document)
            datos.append(document)
    except Exception as e:
        # Registrando un error en caso de que ocurra alguno
        log.error(f'Hubo un error al obtener los datos: {e}')
        raise

    return datos

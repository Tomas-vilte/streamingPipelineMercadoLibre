from pymongo import MongoClient
from loggerBase import log



def getDataOfMongo(limit:int, database: str, coleccion: str, host: str = 'mongodb://root:secret@172.20.0.2', port: int = 27017) -> list:
    """
    :param limit: Limite de registros a devolver.
    :param database: Nombre de la base de datos de mongoDB.
    :param coleccion: Nombre de la coleccion.
    :param host: Host.
    :param port: Puerto de la base de datos.
    :return: Esto retorna una lista con todos los datos en la coleccion.
    """
    datos = []
    try:

        # Creando una conexión con MongoDB
        clients = MongoClient(host=host, port=port)
        log.info(f'Conexion exitosa a la base de datos: {database}')
        # Obteniendo la base de datos especificada
        db = clients[database]
        log.info(f'Obteniendo coleccion: {coleccion}')
        # Obteniendo la colección especificada
        collection = db.get_collection(coleccion)
        # Obteniendo los registros limitados de la colección
        data = collection
        for document in data.find({}).limit(limit=limit):
            print(document)
            datos.append(document)
    except Exception as e:
        # Registrando un error en caso de que ocurra alguno
        log.error(f'Hubo un error al obtener los datos: {e}')

    return datos

from pymongo import MongoClient
from loggin import log

def statusMongo() -> True or False:
    # Si tenes levantado mongoDB en docker, tenes que poner la direccion ip del container con o sin sus credenciales,
    # En caso que tengas mondoDB en tu computadora local sin docker, podes usar mongodb://localhost:27017 o mongodb://121.0.0.1:27017
    # Si usas las credenciales te quedaria asi la url: mongodb://tuUsuario:tuContraseña@localhost:27017 o direccion ip.
    # !Otra cosa importante! Si vas a usar mongodb con o sin docker, y airflow en local esto funciona, pero si vas a usar
    # airflow con docker, tenes que agregar el container de mongoDB a la red de airflow para que funcione.
    client = MongoClient("mongodb://root:secret@172.22.0.8:27017")
    try:
        db_list = client.server_info()
        log.info("Conexion exitosa a mongoDB")
        print(f'Estado del servidor corriendo: {db_list}')
        return True, db_list
    except Exception as error:
        log.error(f"Error al conectar a mongoDB: {error}")
        raise Exception(f'Error al conectar a mongoDB: {error}')
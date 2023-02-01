from loggin import log
import psycopg2


def statusPostgres(user:str, password:str, host:str, database:str, port: int):
    """
    Verifica el estado de la conexión a una base de datos PostgreSQL alojada en AWS RDS.

    :param user: Nombre de usuario para conectarse a la base de datos.
    :param password: Contraseña para conectarse a la base de datos.
    :param host: Host o dirección IP del servidor de la base de datos.
    :param database: Nombre de la base de datos.
    :param port: Puerto utilizado para conectarse a la base de datos.
    :return: None
    """
    try:
        log.info(f'Conexion exitosa a la base de datos de aws rds: {database}')
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print(conn)
    except Exception as error:
        log.error(f'Ocurrio un error al conectarse a la base de datos de aws rds: {error}')


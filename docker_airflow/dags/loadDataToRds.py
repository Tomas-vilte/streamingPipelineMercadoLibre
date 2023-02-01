from loggin import log
import psycopg2
from getDataOfMongo import getDataOfMongo

class DataUploader:
    """
       Clase para subir datos a una base de datos PostgreSQL
    """

    def __init__(self, host, port, dbname, user, password):
        """
        Constructor que inicializa la conexión a AWS RDS
        :param host: el nombre de host o dirección IP de la base de datos
        :param port: el número de puerto para la base de datos
        :param dbname: el nombre de la base de datos
        :param user: el nombre de usuario para conectarse a la base de datos
        :param password: la contraseña para el nombre de usuario
        """
        try:
            log.info(f'Conexion exitosa a la base de datos: {dbname}')
            self.conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password,
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            log.error(f'Hubo un error al conectarse a la base de datos: {e}')

    def upload_data(self, data):
        """
        Método para subir datos a la base de datos
        :param data: los datos a cargar
        """
        try:
            log.info('Cargando datos a la base de datos...')
            for item in data:
                self.cur.execute("SELECT * FROM mytable WHERE id = %s", (item["id"],))
                if self.cur.fetchone() is None:
                    self.cur.execute("INSERT INTO mytable (id, nameofproduct,"
                                     "price, "
                                     "productstatus, "
                                     "sellername, "
                                     "registrationdate,"
                                     "quantitysold,"
                                     "quantityavailable,"
                                     "free_shipping,"
                                     "storeratings) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                     (item["id"], item["nameOfProduct"], item["price"],
                                      item["ProductStatus"], item["SellerName"], item["RegistrationDate"],
                                      item["QuantitySold"], item["QuantityAvailable"], item["Free shipping?"],
                                      item["Store ratings"]))
                    self.conn.commit()
                    log.info(f'Se cargaron correctamente los datos: {item}')
                else:
                    log.info(f'El id {item["id"]} ya existe en la tabla')
        except Exception as e:
            log.error(f'Error al subir los datos a la base de datos: {e}')

    def __del__(self):
        """
        Destructor que cierra el cursor y la conexión.
        """
        self.cur.close()

        self.conn.close()


def uploadData():
    """
    Función para recuperar datos de MongoDB y subirlos a PostgreSQL
    """
    # Obteniendo los datos de MongoDB
    client = getDataOfMongo(limit=50, database='mercadolibredb', coleccion='meliproduct')
    # Cargando los datos obtenidos en una base de datos PostgreSQL
    database = DataUploader(host='mydatabase.cnfp6axcdse9.us-east-1.rds.amazonaws.com', port=5432, dbname='meliAnalytics', user='postgres', password='postgres')
    database.upload_data(client)

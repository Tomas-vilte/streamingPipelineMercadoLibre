import psycopg2
from loggerBase import log

class DataUploader:
    def __init__(self, host, port, dbname, user, password):
        """
        Constructor that initializes the connection to RDS
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
        Destructor that closes the cursor and connection
        """

        self.cur.close()

        self.conn.close()

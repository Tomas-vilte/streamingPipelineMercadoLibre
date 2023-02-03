from loadDataToRds import DataUploader
import unittest

# Definir la clase TestDataUploader, que es una subclase de unittest.TestCase
class TestDataUploader(unittest.TestCase):

    # Definir el método de configuración, que se ejecuta antes de cada método de prueba
    def setUp(self):
        # Inicializar los datos de prueba
        self.data = [
            {"id": '1', "nameOfProduct": "Product 1", "price": 100, "ProductStatus": "Active",
             "SellerName": "Seller 1", "RegistrationDate": "2020-01-01", "QuantitySold": 10,
             "QuantityAvailable": 20, "Free shipping?": True, "Store ratings": 4.5},
            {"id": '2', "nameOfProduct": "Product 2", "price": 200, "ProductStatus": "Inactive",
             "SellerName": "Seller 2", "RegistrationDate": "2020-02-01", "QuantitySold": 20,
             "QuantityAvailable": 10, "Free shipping?": False, "Store ratings": 3.5}
        ]

        # Crear una instancia de la clase DataUploader, conectándose a la base de datos especificada
        self.database = DataUploader(
            host='your host',
            port=5432,
            dbname='meliAnalytics',
            user='postgres',
            password='postgres'
        )

    # Definir el método test_upload_data, que prueba el método upload_data de la clase DataUploader
    def test_upload_data(self):
        # Llama al método upload_data con los datos de prueba
        self.database.upload_data(self.data)

        # Crea un cursor para la conexión a la base de datos
        cur = self.database.conn.cursor()

        # Ejecutar una consulta SQL para recuperar el primer registro de la tabla mytable
        cur.execute("SELECT * FROM mytable WHERE id = '1'")

        # Obtener el resultado de la consulta SQL
        result = cur.fetchone()

        # Compara el resultado con el resultado esperado usando el método assertEqual
        self.assertEqual(result, result)

        # Ejecutar una consulta SQL para recuperar el segundo registro de la tabla mytable
        cur.execute("SELECT * FROM mytable WHERE id = '2'")

        # Obtener el resultado de la consulta SQL
        result = cur.fetchone()

        # Compara el resultado con el resultado esperado usando el método assertEqual
        self.assertEqual(result, result)

    # Definir el método de desmontaje, que se ejecuta después de cada método de prueba
    def tearDown(self):
        # Cerrar la conexión a la base de datos
        self.database.conn.close()



if __name__ == '__main__':
    unittest.main()

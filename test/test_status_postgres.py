import unittest
from postgresStatus import statusPostgres

class TestPostgresStatus(unittest.TestCase):
    """
        Clase de pruebas para verificar la conexión a una base de datos PostgreSQL alojada en AWS RDS.
    """
    def test_statusPostgres(self):
        """
            Prueba para verificar si la conexión a la base de datos es exitosa o no.
        """
        user = 'tomi'
        password = 'tomi'
        host = 'localhost'
        database = 'test'
        port = 5432

        try:
            # Llamar a la función "statusPostgres" y Intentar conectarse a la base de datos
            success, result = statusPostgres(user, password, host, database, port)

            # Verificar que la conexión sea exitosa
            self.assertTrue(success)

            print(f'Conexion exitosa a la base de datos: {result}')
        except Exception as error:
            # Imprimir un mensaje de error si la conexión falla
            self.fail(f'Prueba fallida con error: {error}')

if __name__ == '__main__':
    unittest.main()
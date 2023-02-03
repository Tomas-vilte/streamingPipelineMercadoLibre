import unittest
from getDataOfMongo import getDataOfMongo

# Definimos la clase TestGetDataOfMongo
class TestGetDataOfMongo(unittest.TestCase):

    # Prueba para verificar que el resultado de la función sea una lista
    def test_getDataOfMongo_existing_database(self):
        result = getDataOfMongo(1, 'mercadolibredb', 'meliproduct')
        self.assertIsInstance(result, list)

    # Prueba para verificar que se lanze una excepción si la base de datos no existe
    def test_database_not_found(self):
        limit = 1
        database = 'mercadolibredb123'
        collection = 'meliproduct'
        with self.assertRaises(Exception) as context:
            getDataOfMongo(limit, database, collection)
        self.assertTrue(f"La base de datos {database} no existe" in str(context.exception))

    # Prueba para verificar que se lanze una excepción si la colección no existe
    def test_collection_not_found(self):
        limit = 1
        database = 'mercadolibredb'
        collection = 'meliproduct1234'
        with self.assertRaises(Exception) as context:
            getDataOfMongo(limit, database, collection)
        self.assertTrue(f'La coleccion {collection} no existe en la base de datos {database}' in str(context.exception))

# Verifica si este script se está ejecutando como el programa principal
if __name__ == '__main__':
    # Ejecutamos las pruebas unitarias
    unittest.main()

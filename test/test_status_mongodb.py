import unittest

from mongoStatus import statusMongo

class TestStatusMongo(unittest.TestCase):
    def test_status_mongo(self):
        try:
            result = statusMongo()
            self.assertTrue(result)
            self.assertIsNotNone(result)

        except Exception as error:
            self.fail(f'Prueba fallida con error: {error}')


if __name__ == '__main__':
    unittest.main()
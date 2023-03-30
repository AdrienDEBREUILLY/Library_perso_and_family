import unittest
from flask_testing import TestCase
from app import create_app

class TestRoutes(TestCase):

    def create_app(self):
        app = create_app()
        return app

    def test_index(self):
        response = self.client.get("/")
        self.assert200(response)

    # Ajoutez d'autres tests pour les autres routes

if __name__ == '__main__':
    unittest.main()
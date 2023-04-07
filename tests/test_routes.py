import unittest
from flask_testing import TestCase
from app import create_app


def create_app():
    app = create_app()
    return app


class TestRoutes(TestCase):

    def test_index(self):
        response = self.client.get("/")
        self.assert200(response)

    # Ajoutez d'autres tests pour les autres routes


if __name__ == '__main__':
    unittest.main()
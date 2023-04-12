import unittest
from app import app, db
from app.models import User, Book
from flask import url_for


class TestRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://adrien:adrien@localhost/bibliotheque_perso_and_family'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_book_list(self):
        response = self.app.get('/livre_liste')
        self.assertEqual(response.status_code, 302)

    def test_book_detail(self):
        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        response = self.app.get('/livre_detail/{}'.format(book.id_book))
        self.assertEqual(response.status_code, 302)

    def test_book_add(self):
        response = self.app.get('/livre_ajouter')
        self.assertEqual(response.status_code, 302)

    def test_book_update(self):
        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        response = self.app.get('/livre_modifier/{}'.format(book.id_book))
        self.assertEqual(response.status_code, 302)

    def test_book_delete(self):
        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        response = self.app.post('/livre_supprimer/{}'.format(book.id_book))
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
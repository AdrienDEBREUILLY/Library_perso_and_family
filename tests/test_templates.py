import unittest
from flask import render_template_string
from app import app, db
from app.models import User


class TestTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_context = app.app_context()
        cls.app_context.push()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://adrien:adrien@localhost/test_db'
        cls.client = app.test_client()
        db.create_all()
        cls.create_test_user()
        cls.client.post('/login', data=dict(username='testuser', password='testpassword'), follow_redirects=True)

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    @classmethod
    def create_test_user(cls):
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

    def setUp(self):
        self.transaction = db.session.begin_nested()

    def login(self):
        self.client.post('/login', data=dict(username='testuser', password='testpassword'), follow_redirects=True)

    def tearDown(self):
        self.transaction.rollback()

    def render(self, template, **context):
        with app.test_request_context():
            return render_template_string(template, **context)

    def test_base_template(self):
        template = '''
        {% extends 'base.html' %}
        {% block content %}
        Test content
        {% endblock %}
        '''
        rendered_template = self.render(template)
        self.assertIn('Test content', rendered_template)

    def test_book_add_template(self):
        # Test pour vérifier que le formulaire d'ajout de livre est présent
        response = self.client.get('/livre_ajouter')
        self.assertIn('<input type="submit" value="Ajouter">', response.data.decode())

    def test_index_template(self):
        # Test pour vérifier que la liste des livres est présente
        response = self.client.get('/')
        self.assertIn('<div class="list-group">', response.data.decode())

    def test_login_template(self):
        # Test pour vérifier que le formulaire de connexion est présent
        response = self.client.get('/login')
        self.assertIn('<input type="submit" value="Login"', response.data.decode())

    def test_book_detail_template(self):
        response = self.client.get('/livre_detail/1')
        self.assertIn('Book 1', response.data.decode())
        self.assertIn('Author 1', response.data.decode())
        self.assertIn('Publisher 1', response.data.decode())
        self.assertIn('2023-01-01', response.data.decode())
        self.assertIn('Synopsis for Book 1', response.data.decode())
        self.assertIn('English', response.data.decode())
        self.assertIn('cover1.jpg', response.data.decode())

    def test_book_list_template(self):
        response = self.client.get('/livre_liste')
        self.assertIn('<table class="table table-striped">', response.data.decode())

    def test_book_update_template(self):
        response = self.client.get('/livre_modifier/1')
        self.assertIn('Book 1', response.data.decode())
        self.assertIn('Author 1', response.data.decode())
        self.assertIn('<input type="submit" value="Mettre à jour">', response.data.decode())

    def test_register_template(self):
        response = self.client.get('/register')
        self.assertIn('<input type="submit" value="Register">', response.data.decode())

    def test_nav_template(self):
        response = self.client.get('/')
        self.assertIn('<nav class="navbar navbar-expand-lg navbar-dark bg-dark">', response.data.decode())


if __name__ == "__main__":
    unittest.main()

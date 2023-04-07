import unittest
from app.models import Book, User, BookList


class TestModels(unittest.TestCase):

    def test_create_book(self):
        book = Book(title="Example Book", author="John Doe")
        self.assertEqual(book.title, "Example Book")
        self.assertEqual(book.author, "John Doe")

    def test_create_user(self):
        user = User(username="johndoe", email="johndoe@example.com", password="hashed_password")
        self.assertEqual(user.username, "johndoe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.password, "hashed_password")

    # Ajoutez d'autres tests pour les autres modèles


if __name__ == '__main__':
    unittest.main()

import unittest
from app.models import Book, User, BookList

class TestModels(unittest.TestCase):

    def test_create_book(self):
        book = Book(title="Example Book", author="John Doe")
        self.assertEqual(book.title, "Example Book")
        self.assertEqual(book.author, "John Doe")

    # Ajoutez d'autres tests pour les autres modèles

if __name__ == '__main__':
    unittest.main()
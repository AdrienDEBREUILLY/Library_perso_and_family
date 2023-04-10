import unittest
from app import app, db
from app.models import Users, Book, BookList, BookListBook, Serie, BookSerie, SeriePart, BorrowedBook
from datetime import date


class TestModels(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://adrien:adrien@localhost/bibliotheque_perso_and_family'
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user(self):
        user = Users(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        found_user = Users.query.filter_by(username='testuser').first()
        self.assertIsNotNone(found_user)
        self.assertTrue(found_user.check_password('testpassword'))

    def test_book(self):
        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        found_book = Book.query.filter_by(title='Test Book').first()
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book.author, 'Test Author')

    def test_book_list(self):
        user = Users(username='testuser2', email='test2@example.com')
        user.set_password('testpassword2')
        db.session.add(user)
        db.session.commit()

        book_list = BookList(name='Test BookList', user_id=user.id_users)
        db.session.add(book_list)
        db.session.commit()

        found_book_list = BookList.query.filter_by(name='Test BookList').first()
        self.assertIsNotNone(found_book_list)
        self.assertEqual(found_book_list.user_id, user.id_users)

        # Test BookListBook model
    def test_book_list_book(self):
        book = Book(title='Test Book 2', author='Test Author 2')
        db.session.add(book)
        db.session.commit()

        user = Users(username='testuser3', email='test3@example.com')
        user.set_password('testpassword3')
        db.session.add(user)
        db.session.commit()

        book_list = BookList(name='Test BookList 2', user_id=user.id_users)
        db.session.add(book_list)
        db.session.commit()

        book_list_book = BookListBook(book_id=book.id_book, book_list_id=book_list.id_book_list)
        db.session.add(book_list_book)
        db.session.commit()

        found_book_list_book = BookListBook.query.filter_by(book_id=book.id_book,
                                                                book_list_id=book_list.id_book_list).first()
        self.assertIsNotNone(found_book_list_book)

        # Test Serie model
    def test_serie(self):
        serie = Serie(name='Test Serie')
        db.session.add(serie)
        db.session.commit()

        found_serie = Serie.query.filter_by(name='Test Serie').first()
        self.assertIsNotNone(found_serie)

        # Test BookSerie model
    def test_book_serie(self):
        book = Book(title='Test Book 3', author='Test Author 3')
        db.session.add(book)
        db.session.commit()

        serie = Serie(name='Test Serie 2')
        db.session.add(serie)
        db.session.commit()

        book_serie = BookSerie(book_id=book.id_book, serie_id=serie.id_serie, number_in_serie=1)
        db.session.add(book_serie)
        db.session.commit()

        found_book_serie = BookSerie.query.filter_by(book_id=book.id_book, serie_id=serie.id_serie).first()
        self.assertIsNotNone(found_book_serie)
        self.assertEqual(found_book_serie.number_in_serie, 1)

    # Test SeriePart model
    def test_serie_part(self):
        serie = Serie(name='Test Serie 3')
        db.session.add(serie)
        db.session.commit()

        serie_part = SeriePart(serie_id=serie.id_serie, part_name='Test Part', part_number=1)
        db.session.add(serie_part)
        db.session.commit()

        found_serie_part = SeriePart.query.filter_by(serie_id=serie.id_serie, part_name='Test Part').first()
        self.assertIsNotNone(found_serie_part)
        self.assertEqual(found_serie_part.part_number, 1)

    # Test BorrowedBook model
    def test_borrowed_book(self):
        book = Book(title='Test Book 4', author='Test Author 4')
        db.session.add(book)
        db.session.commit()

        user = Users(username='testuser4', email='test4@example.com')
        user.set_password('testpassword4')
        db.session.add(user)
        db.session.commit()

        borrowed_book = BorrowedBook(user_id=user.id_users, book_id=book.id_book, borrowed_date=date.today())
        db.session.add(borrowed_book)
        db.session.commit()

        found_borrowed_book = BorrowedBook.query.filter_by(user_id=user.id_users, book_id=book.id_book).first()
        self.assertIsNotNone(found_borrowed_book)
        self.assertEqual(found_borrowed_book.borrowed_date, date.today())


if __name__ == "__main__":
    unittest.main()

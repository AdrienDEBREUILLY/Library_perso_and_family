from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id_user)


class Book(db.Model):
    id_book = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50))
    publication_date = db.Column(db.Date)
    synopsis = db.Column(db.Text)
    language = db.Column(db.String(15))
    cover_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}')"


class BookList(db.Model):
    id_book_list = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('book_lists', lazy=True))

    def __repr__(self):
        return f"BookList('{self.name}', '{self.user_id}')"


class BookListBook(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id_book'), primary_key=True)
    book_list_id = db.Column(db.Integer, db.ForeignKey('book_list.id_book_list'), primary_key=True)
    book_added_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    book = db.relationship('Book', backref=db.backref('book_lists', lazy=True))
    book_list = db.relationship('BookList', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return f"BookListBook('{self.book_id}', '{self.book_list_id}')"


class Serie(db.Model):
    id_serie = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"Serie('{self.name}')"


class BookSerie(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id_book'), primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id_serie'), primary_key=True)
    number_in_serie = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    book = db.relationship('Book', backref=db.backref('series', lazy=True))
    serie = db.relationship('Serie', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return f"BookSerie('{self.book_id}', '{self.serie_id}', '{self.number_in_serie}')"


class SeriePart(db.Model):
    id_serie_part = db.Column(db.Integer, primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id_serie'), nullable=False)
    part_name = db.Column(db.String(50), nullable=False)
    part_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    serie = db.relationship('Serie', backref=db.backref('parts', lazy=True))

    def __repr__(self):
        return f"SeriePart('{self.serie_id}', '{self.part_name}', '{self.part_number}')"


class BorrowedBook(db.Model):
    id_borrowed_book = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id_book'), nullable=False)
    borrowed_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    returned_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('borrowed_books', lazy=True))
    book = db.relationship('Book', backref=db.backref('borrowed_books', lazy=True))

    def __repr__(self):
        return f"BorrowedBook('{self.user_id}', '{self.book_id}', '{self.borrowed_date}')"


# Définir un événement qui agit comme un trigger
    # @event.listens_for(BookListBook, 'before_insert')
    # def set_book_added_date(mapper, connection, target):
        # target.book_added_date = func.current_date()

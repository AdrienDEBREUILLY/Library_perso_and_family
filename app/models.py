from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    username = db.Column(db.String(30), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    email = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class Book(db.Model):
    title = db.Column(db.String(50), primary_key=True, nullable=False)
    author = db.Column(db.String(50), primary_key=True, nullable=False)
    publisher = db.Column(db.String(50))
    publication_date = db.Column(db.Date)
    synopsis = db.Column(db.Text)
    language = db.Column(db.String(15))
    cover_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class BookList(db.Model):
    name = db.Column(db.String(50), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class BookListBook(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.title'), primary_key=True, nullable=False)
    book_list_id = db.Column(db.Integer, db.ForeignKey('book_list.name'), primary_key=True, nullable=False)
    book_added_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class Serie(db.Model):
    name = db.Column(db.String(50), primary_key=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class BookSerie(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.title'), primary_key=True, nullable=False)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.name'), primary_key=True, nullable=False)
    number_in_serie = db.Column(db.Integer, primary_key=True, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class SeriePart(db.Model):
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.name'), primary_key=True, nullable=False)
    part_name = db.Column(db.String(50), primary_key=True, nullable=False)
    part_number = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class BorrowedBook(db.Model):
    id_borrowed_book = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.title'), nullable=False)
    borrowed_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    returned_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# Définir un événement qui agit comme un trigger
@event.listens_for(BookListBook, 'before_insert')
def set_book_added_date(mapper, connection, target):
    target.book_added_date = func.current_date()

from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Book, BookList, BookListBook, Serie, BookSerie, BorrowedBook
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, BookForm, BookListForm, SerieForm, BorrowBookForm
from app.main import main


@main.route('/')
@main.route('/home')
def home():
    books = Book.query.all()
    return render_template('index.html', books=books)


@main.route('/book/<string:title>', methods=['GET', 'POST'])
def book_detail(title):
    book = Book.query.get_or_404(title)
    return render_template('book_detail.html', title=book.title, book=book)


@main.route('/book/new', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, publisher=form.publisher.data,
                    publication_date=form.publication_date.data, synopsis=form.synopsis.data,
                    language=form.language.data, cover_url=form.cover_url.data)
        db.session.add(book)
        db.session.commit()
        flash('Your book has been added!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_book.html', title='New Book', form=form, legend='New Book')


@main.route('/book/<string:title>/update', methods=['GET', 'POST'])
@login_required
def update_book(title):
    book = Book.query.get_or_404(title)
    form = BookForm()
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.publisher = form.publisher.data
        book.publication_date = form.publication_date.data
        book.synopsis = form.synopsis.data
        book.language = form.language.data
        book.cover_url = form.cover_url.data
        db.session.commit()
        flash('Your book has been updated!', 'success')
        return redirect(url_for('main.book_detail', title=book.title))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.publisher.data = book.publisher
        form.publication_date.data = book.publication_date
        form.synopsis.data = book.synopsis
        form.language.data = book.language
        form.cover_url.data = book.cover_url
    return render_template('create_book.html', title='Update Book', form=form, legend='Update Book')


@main.route('/book/<string:title>/delete', methods=['POST'])
@login_required
def delete_book(title):
    book = Book.query.get_or_404(title)
    db.session.delete(book)
    db.session.commit()
    flash('Your book has been deleted!', 'success')
    return redirect(url_for('main.home'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@main.route('/booklist', methods=['GET', 'POST'])
@login_required
def booklist():
    form = BookListForm()
    if form.validate_on_submit():
        booklist = BookList(name=form.name.data, user_id=current_user.id)
        db.session.add(booklist)
        db.session.commit()
        flash('Your book list has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('booklist.html', title='Book List', form=form)

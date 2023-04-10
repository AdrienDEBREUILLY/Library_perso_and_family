from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.forms import LoginForm, RegistrationForm, AddBookForm, UpdateBookForm
from app.models import Users, Book

routes = Blueprint('routes', __name__)


# User-related routes
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        print("User found:", user)  # Debugging statement
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print("Password matches")  # Debugging statement
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('routes.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', title='Register', form=form)


@routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))


# Book-related routes
@routes.route('/')
@routes.route('/index')
@login_required
def index():
    print("Authenticated:", current_user.is_authenticated)
    books = Book.query.all()
    return render_template('index.html', books=books)


@routes.route('/livre_liste')
@login_required
def book_list():
    books = Book.query.all()
    return render_template('book_list.html', books=books)


@routes.route('/livre_detail/<int:book_id>')
@login_required
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


# Add, update, and delete book routes from previous response
@routes.route('/livre_ajouter', methods=['GET', 'POST'])
@login_required
def book_add():
    form = AddBookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, user_id=current_user.id_user)
        db.session.add(book)
        db.session.commit()
        flash('Votre livre a été ajouté avec succès!', 'success')
        return redirect(url_for('routes.index'))
    return render_template('livre_ajouter.html', title='Ajouter un livre', form=form)


@routes.route('/livre_modifier/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_update(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.id_user:
        abort(403)
    form = UpdateBookForm()
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        db.session.commit()
        flash('Votre livre a été mis à jour avec succès!', 'success')
        return redirect(url_for('routes.livre_detail', book_id=book.id_book))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
    return render_template('livre_modifier.html', title='Modifier un livre', form=form)


@routes.route('/livre_supprimer/<int:book_id>', methods=['POST'])
@login_required
def book_delete(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.id_user:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('Votre livre a été supprimé avec succès!', 'success')
    return redirect(url_for('routes.index'))


# Error handlers
@routes.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@routes.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403


@routes.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

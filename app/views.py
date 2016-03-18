from builtins import print

from app import app, db
from flask import render_template, redirect, request, session, url_for, g
from flask.ext.login import current_user
from flask.ext.login import LoginManager
from flask.ext.login import login_required, login_user, logout_user
from .forms import *
from .models import User, UserBooks, Book

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.before_request
def before_request():
    g.search_form = NavSearchForm()
    session['search-data'] = g.search_form.content.data

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'email' not in session:
        loginForm = LoginForm()
        return render_template('login.html', title='Sign In', form=loginForm)
    search_str = request.args.get('content', '')
    result = search_by_title(search_str)
    return render_template('book_search_result.html', result_books=result)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        print("User is authenticated")
    else:
        print("User is not authenticated", current_user)
    print(User.query.all())

    loginform = LoginForm()
    read_book_form = AddBookForm()
    unread_book_form = AddBookForm()
    top_books = Book.query.order_by(Book.rating.desc()).limit(5).all()
    return render_template('index.html', loginform=loginform,
                           read_book_form=read_book_form,
                           unread_book_form=unread_book_form,
                           top_books=top_books)


@app.route('/add_read', methods=['GET', 'POST'])
@login_required
def add_read():
    if request.method == 'POST':
        read_book_form = AddBookForm()
        add_book_with_state('read', read_book_form)
    return redirect('/bookshelf')


@app.route('/add_unread', methods=['GET', 'POST'])
@login_required
def add_unread():
    if request.method == 'POST':
        unread_book_form = AddBookForm()
        add_book_with_state('unread', unread_book_form)
    return redirect('/bookshelf')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter(User.email == form.email.data).first()
        print("Prepare to validate")
        if user and user.verify_password(form.password.data):
            session['current_user_id'] = user.id
            session['remember_me'] = form.remember_me.data
            login_user(user, remember=form.remember_me.data)
        else:
            return render_template('login.html', title='Sign In', form=form)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        user = User(email=form.email.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data)
        user.hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/bookshelf')
@login_required
def show_users_books():
    if 'email' not in session:
        return redirect(url_for('login'))
    user = get_current_user()
    if user is None:
        return redirect(url_for('login'))
    return render_template('bookshelf.html',
                           unread_books=get_books_with_state(user.id, 'unread'),
                           read_books=get_books_with_state(user.id, 'read'))


@app.route('/explore')
@login_required
def explore():
    return render_template('explore.html')


def get_current_user():
    if 'email' not in session.keys():
        return None
    return User.query.filter(User.email == session['email']).first()


def add_book_with_state(state, current_form):
    author = current_form.author.data
    title = current_form.title.data

    rating = current_form.rating.data
    if rating == 'None':
        rating = 0
    else:
        rating = float(rating)

    review = current_form.review.data

    already_added_books = Book.query.filter(Book.author == author, Book.title == title)
    book = already_added_books.first()
    # if the book is already in the Book table, just update its rating
    if book is not None:
        book.rating = (book.rating + rating) / (already_added_books.count() + 1)
    else:
        book = Book(author=author, title=title, rating=rating)

    db.session.add(book)

    user = get_current_user()
    ub = UserBooks(user_id=user.id,
                   book_id=book.id,
                   book_state=state,
                   book_rating=rating,
                   book_review=review)

    db.session.add(ub)
    db.session.commit()


def get_books_with_state(uid, state):
    user_books = UserBooks.query.filter(UserBooks.user_id == uid,
                                        UserBooks.book_state == state).all()
    return [book for book in [Book.query.filter(Book.id == user_book.book_id).first()
                              for user_book in user_books]]


def search_by_title(title):
    return Book.query.filter(Book.title.contains(title)).all()


def reccommend():
    pass;

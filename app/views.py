from app import app, db
from flask import render_template, flash, redirect, request, session, url_for, g
from sqlalchemy import desc
from .forms import *
from .models import User, UserBooks, Book
from random import randint, uniform

@app.before_request
def before_request():
    g.user = get_current_user()
    if g.user is not None:
        g.search_form = NavSearchForm()
        session['search-data'] = g.search_form.content.data

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_str = request.args.get('content', '')
    result = search_by_title(search_str)
    return render_template('book_search_result.html', result_books=result)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    loginform = LoginForm()
    read_book_form = AddBookForm()
    unread_book_form = AddBookForm()
    top_books = Book.query.order_by(Book.rating.desc()).limit(5).all()
    return render_template('index.html', loginform = loginform,
                           read_book_form = read_book_form,
                           unread_book_form = unread_book_form,
                           top_books = top_books)


@app.route('/add_read', methods=['GET', 'POST'])
def add_read():
    if request.method == 'POST':
        read_book_form = AddBookForm()
        add_book_with_state('read', read_book_form)
    return redirect('/bookshelf')


@app.route('/add_unread', methods=['GET', 'POST'])
def add_unread():
    if request.method == 'POST':
        unread_book_form = AddBookForm()
        add_book_with_state('unread', unread_book_form)
    return redirect('/bookshelf')

  
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        session['remember_me'] = form.remember_me.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


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
        session['email'] = user.email
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout')
def signout():
    if 'email' not in session:
        return redirect(url_for('login'))
    session.pop('email')
    return redirect(url_for('index'))


@app.route('/bookshelf')
def show_users_books():
    if 'email' not in session:
        return redirect(url_for('login'))
    user = get_current_user()
    if user is None:
        return redirect(url_for('login'))
    return render_template('bookshelf.html',
                           unread_books = get_books_with_state(user.id, 'unread'),
                           read_books = get_books_with_state(user.id, 'read'))

@app.route('/explore')
def explore():
    return render_template('explore.html')

def get_current_user():
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

    already_added_books = Book.query.filter(Book.author == author,Book.title == title)
    book = already_added_books.first()
    # if the book is already in the Book table, just update its rating
    if book is not None:
        book.rating = (book.rating + rating) / (already_added_books.count() + 1)
    else:
        book = Book(author = author, title = title, rating = rating)

    db.session.add(book)

    user = get_current_user()
    ub = UserBooks(user_id = user.id,
                   book_id = book.id,
                   book_state = state,
                   book_rating = rating,
                   book_review = review)

    db.session.add(ub)
    db.session.commit()


def get_books_with_state(uid, state):
    user_books = UserBooks.query.filter(UserBooks.user_id == uid, 
                                        UserBooks.book_state == state).all()
    return [book for book in [Book.query.filter(Book.id == user_book.book_id).first() 
                    for user_book in user_books]]

def search_by_title(title):
    return Book.query.filter(Book.title.contains(title)).all()
						   
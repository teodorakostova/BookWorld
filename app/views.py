from app import app, db
from flask import render_template, flash, redirect, request, session, url_for
from .forms import *
from .models import User, UserBooks, Book


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    loginform = LoginForm()
    read_book_form = AddBookForm()
    unread_book_form = AddBookForm()
    UserBooks.get_books_with_state(UserBooks,'unread')
    return render_template('index.html', loginform=loginform,
                           read_book_form=read_book_form, unread_book_form=unread_book_form)


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

def get_current_user():
    return User.query.filter(User.email == session['email']).first()


def add_book_with_state(state, current_form):
    book = Book(author = current_form.author.data,
                title = current_form.title.data)
    db.session.add(book)
    user = get_current_user()
    rating = current_form.rating.data
    review = current_form.review.data
    ub = UserBooks(user_id = user.id, book_id = book.id, 
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
    
def get_book_rating(bid):
    ratings = [b for b.book_rating in UserBooks.query.filter(UserBooks.book_id == bid).all()]
    return sum(ratings)
                           
def get_top_books(offset):
    pass
    
						   
						   
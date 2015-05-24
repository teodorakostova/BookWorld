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
    if 'email' not in session:
        login()
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


def change_book_state(book_id, new_state):
    book = UserBooks.query.get((get_current_user_id(), book_id))
    book.book_state = new_state
    db.session.commit()


def get_current_user():
    return User.query.filter(User.email == session['email']).first()


def get_books_with_state(state):
    current_user_id = get_current_user().id
    query = """
		SELECT * FROM BOOK
		WHERE id IN (
			SELECT book_id FROM USER_BOOKS ub
			WHERE
			ub.user_id == {} AND
			ub.book_state == {})
	"""
    books_query = query.format(int(current_user_id), '\'{}\''.format(state))
    return db.session.execute(books_query)


def get_book_id_by_state(book, state):
    books_in_state = get_books_with_state(state)
    for b in books_in_state:
        if (book.title, book.author) == (b.title, b.author):
            books_in_state.close()
            return b.id
    books_in_state.close()
    return -1


def add_book_with_state(state, current_form):
    book = Book(author=current_form.author.data, title=current_form.title.data)
    book_id = get_book_id_by_state(book, 'unread')
    # book_id > 0 --> if book is in 'unread' books of this user
    # book_state should be set to 'read'
    if state == 'read' and book_id > 0:
        change_book_state(book_id, 'read')
    else:
        current_user = get_current_user()
        c = UserBooks(book_state=state)
        c.book = book
        current_user.books.append(c)
        db.session.commit()


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
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/bookshelf')
def show_users_books():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('bookshelf.html',
                           unread_books=get_books_with_state('unread'),
                           read_books=get_books_with_state('read'))

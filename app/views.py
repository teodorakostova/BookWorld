from app import app, db
from flask import render_template, flash, redirect, request, session, url_for
from .forms import *
from .models import User, UserBooks, Book


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    add_book_form = AddBookForm()
    if request.method == 'POST':
    	book = Book(title=add_book_form.title.data, author=add_book_form.author.data)
    	current_user = User.query.filter(User.email == session['email']).first()
    	c = UserBooks(book_state='unread')
    	c.book = book
    	current_user.books.append(c)
    	db.session.commit()
    return render_template('index.html', add_book_form=add_book_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        session['remember_me'] = form.remember_me.data
        session['email'] = form.email.data
        return redirect(url_for('index'))  # for profile..
    return render_template('login.html', title='Sign In', form=form,)


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
    current_user = User.query.filter(User.email == session['email']).first()
    query = """
		SELECT * FROM BOOK
		WHERE id IN (
			SELECT book_id FROM USER_BOOKS ub 
			WHERE 
			ub.user_id == {} AND
			ub.book_state == {})
	"""

    unread_books_query = query.format(int(current_user.id), "\"unread\"")
    read_books_query = query.format(int(current_user.id), "\"read\"")

    unread_books = db.session.execute(unread_books_query)
    read_books = db.session.execute(read_books_query)
    print(unread_books)
    return render_template('bookshelf.html', unread_books=unread_books, read_books=read_books)

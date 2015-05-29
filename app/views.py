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
	if request.method == "POST":
		if read_book_form.validate():
			add_read(read_book_form)
			return redirect(url_for('show_users_books'))
		elif unread_book_form.validate():
			add_unread(unread_book_form)
			return redirect(url_for('show_users_books'))
	return render_template('index.html', loginform=loginform,
						   read_book_form=read_book_form, unread_book_form=unread_book_form)


# @app.route('/add_read', methods=['GET', 'POST'])
def add_read(read_book_form):
	# if request.method == 'POST':
	#     read_book_form = AddBookForm()
	print("ADD READ")
	add_book_with_state('read', read_book_form)


# @app.route('/add_unread', methods=['GET', 'POST'])
def add_unread(unread_book_form):
	# if request.method == 'POST':
	#     unread_book_form = AddBookForm()
	add_book_with_state('unread', unread_book_form)
	



def get_current_user():
	return User.query.filter(User.email == session['email']).first()


def add_book_with_state(state, current_form):
	book = Book(author=current_form.author.data, title=current_form.title.data)
	current_user = get_current_user()
	current_user.add_book(book, state)


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
	user = get_current_user()
	return render_template('bookshelf.html',
						   unread_books=user.get_books_with_state('unread'),
						   read_books=user.get_books_with_state('read'))

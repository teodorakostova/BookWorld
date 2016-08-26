from flask import render_template, redirect, request, session, url_for, flash, g
from flask.ext.login import current_user
from flask.ext.login import LoginManager
from flask.ext.login import login_required, login_user, logout_user
from builtins import print
from .forms import *
from .ViewsUtils import *
from .BookManager import BookManager
from .BooksServiceHelper import RequestHelper

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.before_request
def before_request():
    g.search_form = NavSearchForm()
    session['search-data'] = g.search_form.content.data


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        print("User is authenticated")
    else:
        print("User is not authenticated", current_user)
    login_form = LoginForm()
    read_book_form = AddBookForm()
    unread_book_form = AddBookForm()
    top_books = Book.query.order_by(Book.rating.desc()).limit(10).all()
    return render_template('index.html', loginform=login_form,
                           read_book_form=read_book_form,
                           unread_book_form=unread_book_form,
                           top_books=top_books)


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_content = request.args.get('content', '')
    result = search_by_content(search_content, 10)
    return render_template('book_search_result.html', result_books=result)


@app.route('/add_read', methods=['GET', 'POST'])
@login_required
def add_read():
    if request.method == 'POST':
        read_book_form = AddBookForm()
        add_book_from_form('read', read_book_form)
    else:
        add_book_with_state_from_request('read', request)

    return redirect('/bookshelf')


@app.route('/add_unread', methods=['GET', 'POST'])
@login_required
def add_unread():
    if request.method == 'POST':
        unread_book_form = AddBookForm()
        add_book_from_form('unread', unread_book_form)
    else:
        add_book_with_state_from_request('unread', request)
    return redirect('/bookshelf')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.verify_password(form.password.data):
            session['current_user_id'] = user.id
            session['remember_me'] = form.remember_me.data
            login_user(user, remember=form.remember_me.data)
            flash("You logged in successfully")
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
    flash("You logged out")
    return redirect(url_for('index'))


@app.route('/bookshelf')
@login_required
def show_users_books():
    user = current_user
    return render_template('bookshelf.html',
                           unread_books=get_books_with_state(user.id, 'unread'),
                           read_books=get_books_with_state(user.id, 'read'))


@app.route('/explore')
@login_required
def explore():
    # TODO: Check if the user has read these books
    # TODO: Filter results by genre
    # TODO Implement a real recommendation algorithm...
    return render_template('explore.html', result_books=recommend())

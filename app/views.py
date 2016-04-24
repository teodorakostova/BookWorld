from app import app, db
from flask import render_template, redirect, request, session, url_for, flash, g
from flask.ext.login import current_user
from flask.ext.login import LoginManager
from flask.ext.login import login_required, login_user, logout_user
from builtins import print
from .BookManager import BookManager
from .BooksServiceHelper import RequestHelper
from .forms import *
from .models import User, UserBooks, Book

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
    print(User.query.all())

    loginform = LoginForm()
    read_book_form = AddBookForm()
    unread_book_form = AddBookForm()
    top_books = Book.query.order_by(Book.rating.desc()).limit(5).all()
    return render_template('index.html', loginform=loginform,
                           read_book_form=read_book_form,
                           unread_book_form=unread_book_form,
                           top_books=top_books)


@app.route('/search', methods=['GET', 'POST'])
def search():
    # search_content = request.args.get('content', '')
    # book_manager = BookManager()
    # request_helper = RequestHelper()
    # request_helper.add_item(None, "volumeInfo")
    # request_helper.add_items("volumeInfo", "title", "authors", "categories", "imageLinks", "description")
    # request_helper.max_results(10)
    # request_helper.query(search_content)
    # result = book_manager.search(request_helper)
    result = {'items': [
        {'volumeInfo': {'authors': ['Харпър Ли', 'Цветан Стоянов', 'Ани Бобева'], 'title': 'Да убиеш присмехулник'}},
        {'volumeInfo': {'authors': ['Харпър Ли'], 'title': 'Да убиеш присмехулник'}}, {
            'volumeInfo': {'categories': ['Drama'], 'authors': ['Harper Lee'], 'imageLinks': {
                'thumbnail': 'http://books.google.com/books/content?id=0NEbHGREK7cC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
                'smallThumbnail': 'http://books.google.com/books/content?id=0NEbHGREK7cC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api'},
                           'description': 'Required reading in most high schools, this Pulitzer Prize winning novel was originally published in 1969 and was voted the best book of the century by Library Journal.',
                           'title': 'To Kill a Mockingbird'}}, {
            'volumeInfo': {'categories': ['Fiction'], 'authors': ['Joyce Milton', 'Harper Lee'], 'imageLinks': {
                'thumbnail': 'http://books.google.com/books/content?id=HgdIGqYrXj0C&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
                'smallThumbnail': 'http://books.google.com/books/content?id=HgdIGqYrXj0C&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api'},
                           'description': 'A guide to reading "To Kill A Mockingbird" with a critical and appreciative mind. Includes background on the author\'s life and times, sample tests, term paper suggestions, and a reading list.',
                           'title': "Harper Lee's To Kill a Mockingbird"}}, {
            'volumeInfo': {'authors': ['Christopher Sergel'], 'imageLinks': {
                'thumbnail': 'http://books.google.com/books/content?id=P6bzCgUuVroC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
                'smallThumbnail': 'http://books.google.com/books/content?id=P6bzCgUuVroC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api'},
                           'categories': ['Performing Arts'], 'title': 'To Kill a Mockingbird'}}, {
            'volumeInfo': {'categories': ['Fathers and daughters in literature'],
                           'authors': ['Harold Bloom', 'Harper Lee'], 'imageLinks': {
                    'thumbnail': 'http://books.google.com/books/content?id=LaMTiorjM9cC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
                    'smallThumbnail': 'http://books.google.com/books/content?id=LaMTiorjM9cC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api'},
                           'description': "The Crucible still has permanence and relevance a half century after its initial publication. This powerful political drama set amidst the Salem witch trials is commonly understood as Arthur Miller's poignant response to McCarthyism. This new edition featuring new critical essays examines this important work.",
                           'title': "Harper Lee's To Kill a Mockingbird"}}, {
            'volumeInfo': {'categories': ['Literary Criticism'], 'authors': ['Michael J. Meyer'], 'imageLinks': {
                'thumbnail': 'http://books.google.com/books/content?id=RyJtJZPX8jwC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
                'smallThumbnail': 'http://books.google.com/books/content?id=RyJtJZPX8jwC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api'},
                           'description': "In 1960, To Kill a Mockingbird was published to critical acclaim. To commemorate To Kill a Mockingbird's 50th anniversary, Michael J. Meyer has assembled a collection of new essays that celebrate this enduring work of American literature. These essays approach the novel from educational, legal, social, and thematic perspectives. Harper Lee's only novel won the Pulitzer Prize and was transformed into a beloved film starring Gregory Peck as Atticus Finch. An American classic that frequently appears in middle school and high school curriculums, the novel has been subjected to criticism for its subject matter and language. Still relevant and meaningful, To Kill a Mockingbird has nonetheless been under-appreciated by many critics. There are few books that address Lee's novel's contribution to the American canon and still fewer that offer insights that can be used by teachers and by students. These essays suggest that author Harper Lee deserves more credit for skillfully shaping a masterpiece that not only addresses the problems of the 1930s but also helps its readers see the problems and prejudices the world faces today. Intended for high school and undergraduate usage, as well as for teachers planning to use To Kill a Mockingbird in their classrooms, this collection will be a valuable resource for all teachers of American literature.",
                           'title': "Harper Lee's To Kill a Mockingbird"}}, {
            'volumeInfo': {'categories': ['Alabama'], 'authors': ['Christopher Sergel', 'Harper Lee'], 'imageLinks': {
                'thumbnail': 'http://books.google.com/books/content?id=c9pbL5epUN4C&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
                'smallThumbnail': 'http://books.google.com/books/content?id=c9pbL5epUN4C&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api'},
                           'description': '"In his play, Christopher Sergel has shifted the focus slightly. The result of this shift, I believe, hightlights the novel\'s universal qualities. [He] reminds us...that the issues explored are not those of a \'regional\' work of art (as the novel is often categorised) but are of importance in Nottingham, Manchester, Birmingham or wherever the play is seen by an audience." - from Ray Speakman\'s introduction.',
                           'title': 'The Play of To Kill a Mockingbird'}}, {
            'volumeInfo': {'categories': ['Literary Criticism'], 'authors': ['Claudia Durst Johnson'], 'imageLinks': {
                'thumbnail': 'http://books.google.com/books/content?id=aeqIV1m_akQC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
                'smallThumbnail': 'http://books.google.com/books/content?id=aeqIV1m_akQC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api'},
                           'description': 'Collects documents and commentary illuminating Southern life in the 1950s',
                           'title': 'Understanding To Kill a Mockingbird'}}, {
            'volumeInfo': {'categories': ['Study Aids'], 'authors': ['Anita Price Davis'], 'imageLinks': {
                'thumbnail': 'http://books.google.com/books/content?id=sziIMy_rAIgC&printsec=frontcover&img=1&zoom=1&source=gbs_api',
                'smallThumbnail': 'http://books.google.com/books/content?id=sziIMy_rAIgC&printsec=frontcover&img=1&zoom=5&source=gbs_api'},
                           'description': "REA's MAXnotes for Harper Lee's To Kill a Mockingbird MAXnotes offer a fresh look at masterpieces of literature, presented in a lively and interesting fashion. Written by literary experts who currently teach the subject, MAXnotes will enhance your understanding and enjoyment of the work. MAXnotes are designed to stimulate independent thought about the literary work by raising various issues and thought-provoking ideas and questions. MAXnotes cover the essentials of what one should know about each work, including an overall summary, character lists, an explanation and discussion of the plot, the work's historical context, illustrations to convey the mood of the work, and a biography of the author. Each chapter is individually summarized and analyzed, and has study questions and answers.",
                           'title': 'To Kill a Mockingbird (MAXNotes Literature Guides)'}}]}
    return render_template('book_search_result.html', result_books=result)


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
    return render_template('explore.html')


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

    user = current_user
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

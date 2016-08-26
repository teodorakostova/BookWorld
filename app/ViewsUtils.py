from app import app, db
from flask import render_template, redirect, request, session, flash
from flask.ext.login import current_user
from .models import Book, UserBooks, User
from sqlalchemy import exc, func, desc
from .BooksServiceHelper import RequestHelper
from .BookManager import BookManager

def add_book_from_form(state, current_form):
    author = current_form.author.data
    title = current_form.title.data
    rating = current_form.rating.data
    review = current_form.review.data
    add_book_with_state(state, author, title, rating, review)


def add_book_with_state(state, author, title, rating, review):
    if rating == 'None':
        rating = 0
    else:
        rating = float(rating)

    already_added_books = Book.query.filter(Book.author == author, Book.title == title)
    book = already_added_books.first()
    # if the book is already in the Book table, update its rating
    if book is not None:
        book.rating = (book.rating + rating) / (already_added_books.count() + 1)
    else:
        book = Book(author=author, title=title, rating=rating)

    db.session.add(book)
    db.session.commit()
    user = current_user
    ub = UserBooks(user_id=user.id,
                   book_id=book.id,
                   book_state=state,
                   book_rating=rating,
                   book_review=review)

    db.session.add(ub)
    try:
        db.session.commit()
    except exc.IntegrityError as e:
        flash("You have already added this book.", "error")
        return redirect('/index')


def add_book_with_state_from_request(state, request):
    title = request.args.get('title')
    author = request.args.get('author')
    rating = 0
    review = ''
    add_book_with_state('read', title, author, rating, review)


def get_books_with_state(uid, state):
    user_books = UserBooks.query.filter(UserBooks.user_id == uid,
                                        UserBooks.book_state == state).all()
    return [book for book in [Book.query.filter(Book.id == user_book.book_id).first()
                              for user_book in user_books]]


def search_by_title(title):
    return Book.query.filter(Book.title.contains(title)).all()


def get_high_rated(user, start, limit):
    top_books = Book.query.order_by(Book.rating.desc()).limit(limit).all()
    return top_books


def favourite_author(user):
    user_books_ids = db.session.query(UserBooks.book_id).filter(UserBooks.user_id == user.id).all()
    user_books_ids = [ub[0] for ub in user_books_ids]
    authors_favourite = db.session.query(Book, func.count(Book.author).label('author_occurrence')) \
        .filter(Book.id.in_(user_books_ids)) \
        .group_by(Book.author) \
        .order_by(desc('author_occurrence')).all()
    result = [item[0].author for item in authors_favourite]
    print(result)
    return result


def recommend():
    recommended = []
    favourite_authors = favourite_author(current_user)
    for author in favourite_authors:
        recommended.append(search_by_content(author, 1))

    #print(str(recommended).encode("utf-8"))
    return recommended


def search_by_author(author):
    pass


def search_by_content(content, limit):
    book_manager = BookManager()
    request_helper = RequestHelper()
    request_helper.add_item(None, "volumeInfo")
    request_helper.add_items("volumeInfo", "title", "authors", "categories", "imageLinks", "description")
    request_helper.max_results(limit)
    request_helper.query(content)
    result = book_manager.search(request_helper)
    return result

from app import app, db
from flask import render_template, redirect, request, session, flash
from flask.ext.login import current_user
from .models import Book, UserBooks, User
from sqlalchemy import exc


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
    # if the book is already in the Book table, just update its rating
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


def reccommend():
    pass;

from app import db
from passlib.apps import custom_app_context
import os
from sqlalchemy.orm import relationship, backref
from sqlalchemy import UniqueConstraint

class BookWasAlreadyReadException(Exception):
    pass


class UserBooks(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    book_state = db.Column(db.String(10))
    book_rating = db.Column(db.Integer)
    book_review = db.Column(db.String(200))
    book = relationship("Book", backref='user_assocs')

    def __repr__(self):
        return "Book_id: {}, User_id: {}, State: {}\n".format(self.book_id,
                                                            self.user_id, self.book_state)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    books = relationship(UserBooks, backref='user')
    __table_args__ = (UniqueConstraint('email'),)

    def __repr__(self):
        return 'User: %r' % (self.email)

    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    def get_books_with_state(self, state):
        return [(b.book.title, b.book.author) for b in self.books if b.book_state == state]

    def is_book_in_state(self, book, state):
        return ((book.title, book.author) in self.get_books_with_state(state))

    def change_book_state(self,book_id, new_state):
        book = UserBooks.query.filter(UserBooks.user_id == self.id, UserBooks.book_id == book_id).first()
        book.book_state = new_state
        db.session.commit()

    def add_book(self, book, state, rating=0, review=""):
        if state == 'read' and self.is_book_in_state(book,'unread'):
            book_id = Book.query.filter(Book.title == book.title, Book.author == book.author).first().id
            self.change_book_state(book_id, 'read')
            return
        elif state == 'unread' and self.is_book_in_state(book,'read'):
            raise BookWasAlreadyReadException()
        else:
            c = UserBooks(book_id=book.id, 
                user_id=self.id,book_state=state, book_rating=rating, book_review=review)
            c.book = book
            self.books.append(c)
            db.session.commit()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    author = db.Column(db.String(64))
    __table_args__ = (UniqueConstraint('title', 'author'),)

    def __repr__(self):
        return "ID: {} Title: {}, Author: {}\n".format(self.id,self.title, self.author)

    
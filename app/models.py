from app import db
from passlib.apps import custom_app_context
import os
from sqlalchemy.orm import relationship, backref
from sqlalchemy import UniqueConstraint
from flask.ext.login import UserMixin

class BookWasAlreadyReadException(Exception):
    pass


class UserBooks(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    book_state = db.Column(db.String(10))
    book_rating = db.Column(db.Integer)
    book_review = db.Column(db.String(200))
    #book = relationship("Book", backref='user_assocs')

    def __repr__(self):
        return "Book_id: {}, User_id: {}, State: {}\n".format(self.book_id,
                                                            self.user_id, self.book_state)

                                                            
class User(db.Model, UserMixin):
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



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    author = db.Column(db.String(64))
    genre = db.Column(db.String(64))
    rating = db.Column(db.Float)
    __table_args__ = (UniqueConstraint('title', 'author'),)


    def __repr__(self):
        return "{}, by: {} Rating: {} ".format(self.title, self.author, self.rating)


    
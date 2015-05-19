from app import db
from passlib.apps import custom_app_context
import os
from sqlalchemy.orm import relationship, backref 


class UserBooks(db.Model):
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
	book_state = db.Column(db.String(10))
	book = relationship("Book", backref='user_assocs')
	

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(20))
	firstname = db.Column(db.String(20))
	lastname = db.Column(db.String(20))
	books = relationship(UserBooks, backref='user')
	
	def __repr__(self):
		return 'User: %r' % (self.email)

	def hash_password(self, password):
		self.password = custom_app_context.encrypt(password)

	def verify_password(self, password):
		return custom_app_context.verify(password, self.password)

	def load_user(self, id):
		return User.query.get(int(id))

	

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	author = db.Column(db.String(64))
	rating = db.Column(db.Integer)
	
	def __repr__(self):
		return 'Book: %r' % (self.title)


from app import db, models, views, forms
import sqlalchemy
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, UserBooks, Book


class TestCase(unittest.TestCase):

	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
			os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_db_taken_email(self):
		u = User(firstname='john', email='john@example.com')
		db.session.add(u)
		db.session.commit()
		d = User(firstname='john', email='john@example.com')
		db.session.add(d)
		with self.assertRaises(sqlalchemy.exc.IntegrityError):
			db.session.commit()

	def test_add_read_twice(self):
		u = User(email="aa@example.com")
		db.session.add(u)

		b = Book(title="To Kill A Mocking Bird", author="Harper Lee")
		c = Book(title="To Kill A Mocking Bird", author="Harper Lee")
		u.add_book(b, 'read')
		with self.assertRaises(sqlalchemy.exc.IntegrityError):
			u.add_book(c, 'read')
	
	def test_add_unread_twice(self):
		u = User(email="aa@example.com")
		db.session.add(u)

		b = Book(title="To Kill A Mocking Bird", author="Harper Lee")
		c = Book(title="To Kill A Mocking Bird", author="Harper Lee")
		u.add_book(b, 'unread')
		with self.assertRaises(sqlalchemy.exc.IntegrityError):
			u.add_book(c, 'unread')

	def test_change_unread_to_read(self):
		u = User(email="aa@example.com")
		db.session.add(u)
		c = Book(title="It", author="St. King")
		u.add_book(c, 'unread')
		b = Book(title="It", author="St. King")
		u.add_book(b, 'read')
		assert len(u.get_books_with_state('unread')) == 0

	def test_add_unread_when_read(self):
		u = User(email="aa@example.com")
		db.session.add(u)
		c = Book(title="It", author="St. King")
		u.add_book(c, 'read')
		b = Book(title="It", author="St. King")
		with self.assertRaises(models.BookWasAlreadyReadException):
			u.add_book(b, 'unread')

	

if __name__ == '__main__':
	unittest.main()

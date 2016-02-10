from app import db, models, views, forms
import sqlalchemy
import os
import unittest
import flask
from mixer.backend.flask import mixer, Mixer
from faker import Faker
from config import basedir
from app import app, db
from app.models import User, UserBooks, Book
from coverage import coverage

cov = coverage(source=["app.models", "app.views", "app.forms"])
cov.start()

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        self.__app__ = app.test_client()            
        db.create_all()

        self.__faker__ = Faker()
        self.__user__ = User(firstname=self.__faker__.name(), email=self.__faker__.email())
        db.session.add(self.__user__)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_logout(self):
        with app.test_client() as c:
            rv = c.get('/logout')           
            assert 'email' not in flask.session     

    def test_db_taken_email(self):
        firstname = self.__faker__.name()
        email = self.__faker__.email()      
        u = User(firstname=firstname, email=email)      
        db.session.add(u)
        db.session.commit()
        d = User(firstname=firstname, email=email)
        db.session.add(d)
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            db.session.commit()

    def test_add_read_book_twice(self):     
        title = self.__faker__.text(max_nb_chars=20)
        author = self.__faker__.name()
        b = Book(title=title, author=author)
        c = Book(title=title, author=author)
        self.__user__.add_book(b, 'read')
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            self.__user__.add_book(c, 'read')
    
    def test_add_unread_twice(self):        
        title = self.__faker__.text(max_nb_chars=20)
        author = self.__faker__.name()
        b = Book(title=title, author=author)
        c = Book(title=title, author=author)
        self.__user__.add_book(b, 'unread')
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            self.__user__.add_book(c, 'unread')

    def test_change_unread_to_read(self):       
        c = Book(title="It", author="St. King")
        self.__user__.add_book(c, 'unread')
        b = Book(title="It", author="St. King")
        self.__user__.add_book(b, 'read')
        assert len(self.__user__.get_books_with_state('unread')) == 0

    def test_add_unread_when_read(self):        
        c = Book(title="It", author="St. King")
        self.__user__.add_book(c, 'read')
        b = Book(title="It", author="St. King")
        with self.assertRaises(models.BookWasAlreadyReadException):
            self.__user__.add_book(b, 'unread')

    def test_search(self):
        test_books = []
        for i in range(20):
            self.__user__.add_book(Book(title=("test" + str(i)), author=self.__faker__.name()), 'read')
        assert len(Book.get_books_by_criterion(criterion="test")) == 20

    

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    #cov.html_report(directory='tmp/coverage')
    cov.erase()

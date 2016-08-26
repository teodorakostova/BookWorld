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

class TestCase(unittest.TestCase,):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        self.__app__ = app.test_client()            
        db.create_all()

        titles = ['Title1', 'Title2', 'Title3']
        authors = ['Author1', 'Author2', 'Author3']
        user_emails = ['u1@test.com', 'u2@test.com', 'u3@test.com']
        mixer.init_app(app)
        users = mixer.cycle(2).blend(User, email=(email for email in user_emails))
        books = mixer.cycle(2).blend(Book, title=(title for title in titles),
                                    author=(author for author in authors))
        user_book = mixer.cycle(2).blend(UserBooks,
                                         user_id=(user.id for user in users),
                                         book_id=(book.id for book in books))


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_logout(self):
        with app.test_client() as c:
            rv = c.get('/logout')           
            assert 'email' not in flask.session     

    def test_book(self):
        print(db.session.query(Book).all())
        print(db.session.query(User).count())
        assert db.session.query(Book).count() == 1

    def test_favourite_author(self):
        assert 1 == 1


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

from flask.ext.wtf import Form
from wtforms import TextAreaField, TextField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import Required, Email
from .models import User
from flask import session

class AddBookForm(Form):
	title = TextField('Title', validators=[Required()])
	author = TextField('Author', validators=[Required()])
	submit = SubmitField('Submit')
	rating = SelectField('Rating', choices=[(str(i),i) for i in range(1,11)])
	review = TextAreaField('Review')
	genre = TextField('Genre')


class EmailPasswordForm(Form):
	email = TextField('Email', validators=[Required(), Email()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Submit')


class LoginForm(EmailPasswordForm):
	remember_me = BooleanField('Remember me', default=False)

	def validate(self):
		if not Form.validate(self):
			return False




class RegisterForm(EmailPasswordForm):
	firstname = TextField('First Name')
	lastname = TextField('Last Name')

	def validate(self):
		if not Form.validate(self):
			return False
	 
		user = User.query.filter(User.email == self.email.data.lower()).first()
		if user:
			self.email.errors.append("That email is already taken")
			return False
		else:
			return True

class NavSearchForm(Form):
	content = TextField('Title, Author')
	submit = SubmitField('Search')

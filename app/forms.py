from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email
from .models import User
from flask import session


class AddBookForm(Form):
	title = TextField("Title", validators=[Required()])
	author = TextField("Author", validators=[Required()])
	submit = SubmitField('Submit')


class EmailPasswordForm(Form):
	email = TextField('Email', validators=[Required(), Email()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Submit')


class LoginForm(EmailPasswordForm):
	remember_me = BooleanField('Remember me', default=False)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()

		if user and user.verify_password(self.password.data):
			print("USERID:", user.id)
			session['current_user_id'] = user.id
			return True
		else:
			self.email.errors.append("Invalid e-mail or password")
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

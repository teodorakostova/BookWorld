from wtforms import ValidationError

class Unique():
	def __init__(self, model, field):
		self.model = model
		self.field = field

	def __call__(self, form, filed):
		check = self.model.query.filter(self.field = field.data).first()
		if check not None:
			raise ValidationError('This element already exists')
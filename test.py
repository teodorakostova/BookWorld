from app import db, models, views


def add_users():
	u = models.User(email='john@email.com', password='123')
	b = models.User(email='asd@fw.com', password='13243')
	db.session.add(u)
	db.session.add(b)
	db.session.commit()


def select_all_users():
	users = db.session.execute('SELECT * FROM USER')
	for u in users:
		print(u.id, u.email)



def drop_tables():
	# usersBooks = models.UserBooks.query.all()
	# for b in usersBooks:
	# 	db.session.delete(b)
	books = models.UserBooks.query.all()
	for b in books:
		db.session.delete(b)

	db.session.commit()


def main():
	
	# b1 = models.Book(title="aaa", author="AAA")
	# b2 = models.Book(title="bbb", author="BBB")
	# b3 = models.Book(title="ccc", author="CCC")

	# u = models.User.query.filter(models.User.email == "teddyk94@mail.bg").first()
	# #b = models.User(email='asd@fw.com')
	
	# read = models.UserBooks(book_state="read")
	# c = models.UserBooks(book_state='unread')
	
	# # #read.book = b1
	# c.book = b3
	# c.book = b1
	# c.book = b2


	# # u.books.append(read)
	# u.books.append(c)
	# # u.books.append(c)

	# db.session.add(u)
	# db.session.commit()

	# for assoc in u.books:
	# 	print (assoc.book_state, assoc.book)
	# users = db.session.execute('SELECT * FROM USER_BOOKS')
	# for u in users:
	# 	print(u.user_id, u.book_id, u.book_state)

	#db.drop_all()
	drop_tables()
	#add_users()
	#select_all_users()
	#drop_tables()

if __name__ == '__main__':
	main()

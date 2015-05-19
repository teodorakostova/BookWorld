from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
book = Table('book', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=64)),
    Column('author', String(length=64)),
    Column('rating', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=120)),
    Column('password', String(length=20)),
    Column('firstname', String(length=20)),
    Column('lastname', String(length=20)),
)

user_books = Table('user_books', post_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('book_id', Integer, primary_key=True, nullable=False),
    Column('book_state', String(length=10)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].create()
    post_meta.tables['user'].create()
    post_meta.tables['user_books'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].drop()
    post_meta.tables['user'].drop()
    post_meta.tables['user_books'].drop()

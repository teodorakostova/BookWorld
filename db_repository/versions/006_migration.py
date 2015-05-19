from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user_books = Table('user_books', post_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('book_id', Integer, primary_key=True, nullable=False),
    Column('book_state', String(length=10)),
)

book = Table('book', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=64)),
    Column('author', VARCHAR(length=64)),
    Column('rating', INTEGER),
    Column('user_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user_books'].create()
    pre_meta.tables['book'].columns['user_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user_books'].drop()
    pre_meta.tables['book'].columns['user_id'].create()

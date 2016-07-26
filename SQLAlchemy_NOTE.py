
#--------------------------SQLAlchemy直接参考 => http://docs.sqlalchemy.org/en/latest/orm/tutorial.html----------------------------#

#------------------------------------SQLAlchemy's doc is a little mess??->troublesome to NOTE it!----------------------------------#

#---------------------------熟练使用各种框架是很重要,但绝不是写代码的最重点,只是工具而已.python代码本身更重要----------------------#

# To connect DB we use create_engine():
>>> from sqlalchemy import create_engine
>>> engine = create_engine('sqlite:///:memory:', echo=True)
# The echo flag is a shortcut to setting up SQLAlchemy logging, which is accomplished via Python¡¯s standard 
# logging module. With it enabled, we¡¯ll see all the generated SQL produced.


# declarative base class:
>>> from sqlalchemy.ext.declarative import declarative_base
>>> Base = declarative_base()


# define Tables:
>>> from sqlalchemy import Column, Integer, String
>>> class User(Base):
...     __tablename__ = 'users'
...
...     id = Column(Integer, primary_key=True)
...     name = Column(String)
...     fullname = Column(String)
...     password = Column(String)
...
...     def __repr__(self):
...        return "<User(name='%s', fullname='%s', password='%s')>" % (
...                             self.name, self.fullname, self.password)


# create tables in DB:
>>> Base.metadata.create_all(engine)


# Create an Instance of the Mapped Class:
>>> ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
>>> ed_user.name
'ed'
>>> ed_user.password
'edspassword'
>>> str(ed_user.id)
'None'


# Creating a Session:
>>> from sqlalchemy.orm import sessionmaker
>>> Session = sessionmaker(bind=engine)
# Then, whenever you need to have a conversation with the database, you instantiate a Session:
>>> session = Session()
# The above Session is associated with our SQLite-enabled Engine, but it hasn’t opened any connections
# yet. When it’s first used, it retrieves a connection from a [pool of connections] maintained by the 
# Engine, and holds onto it until we commit all changes and/or close the session object.


# Adding and Updating Objects to session:
>>> ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
>>> session.add(ed_user)

>>> session.add_all([
...     User(name='wendy', fullname='Wendy Williams', password='foobar'),
...     User(name='mary', fullname='Mary Contrary', password='xxg527'),
...     User(name='fred', fullname='Fred Flinstone', password='blah')])


# We tell the Session to issue all remaining changes to the database and commit the transaction
>>> session.commit()
# The connection resources referenced by the session are now returned to the connection pool. Subsequent operations with this session
# will occur in a new transaction, which will again re-acquire connection resources when first needed.


# Rolling Back
# Since the Session works within a transaction, we can roll back changes made too.
>>> session.rollback()


# Querying
# A Query object is created using the query() method on Session. 
>>> session.query(User).filter_by(name = 'ed')
>>> session.query(User).filter(User.name == 'ed')
>>> session.query(User.name, User.fullname).all()

















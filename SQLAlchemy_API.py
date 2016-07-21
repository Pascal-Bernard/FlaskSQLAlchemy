from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from SQLAlchemy_define_model import Address, Base, Person
engine = create_engine('sqlite:///sqlalchemy_example.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
# Insert a Person in the person table
new_person = Person(name='new person')
session.add(new_person)
session.commit()
# Insert an Address in the address table
new_address = Address(post_code='00000', person=new_person)
session.add(new_address)
session.commit()

##------------------------------------------------------------------##
from sqlalchemy_declarative import Person, Base, Address
from sqlalchemy import create_engine
engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
# Make a query to find all Persons in the database
session.query(Person).all()
#[<sqlalchemy_declarative.Person object at 0x2ee3a10>]
 
# Return the first Person from all Persons in the database
person = session.query(Person).first()
person.name
#u'new person'
 
# Find all Address whose person field is pointing to the person object
session.query(Address).filter(Address.person == person).all()
#[<sqlalchemy_declarative.Address object at 0x2ee3cd0>]
 
# Retrieve one Address whose person field is point to the person object
session.query(Address).filter(Address.person == person).one()
#<sqlalchemy_declarative.Address object at 0x2ee3cd0>
address = session.query(Address).filter(Address.person == person).one()
address.post_code
#u'00000'
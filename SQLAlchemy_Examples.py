'''
pure SQL:

BEGIN TRANSACTION;
DROP TABLE IF EXISTS Cars;

CREATE TABLE Cars(Id INTEGER PRIMARY KEY, Name TEXT, Price INTEGER);
INSERT INTO Cars VALUES(1, 'Audi', 52642);
INSERT INTO Cars VALUES(2, 'Mercedes', 57127);
INSERT INTO Cars VALUES(3, 'Skoda', 9000);
INSERT INTO Cars VALUES(4, 'Volvo', 29000);
INSERT INTO Cars VALUES(5, 'Bentley', 350000);
INSERT INTO Cars VALUES(6, 'Citroen', 21000);
INSERT INTO Cars VALUES(7, 'Hummer', 41400);
INSERT INTO Cars VALUES(8, 'Volkswagen', 21600);
COMMIT;
'''

##------------------------------------------------------------------##  SOME ORM Examples ==>>
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

##------------------------------------------------------------------##
#Raw SQL
from sqlalchemy import create_engine

eng = create_engine('sqlite:///:memory:')

with eng.connect() as con:
    
    rs = con.execute('SELECT 5')
        
    data = rs.fetchone()[0]
    
    print "Data: %s" % data  
##------------------------------------------------------------------##
from sqlalchemy import create_engine

eng = create_engine('postgresql:///testdb')
con = eng.connect()

rs = con.execute("SELECT VERSION()")
print rs.fetchone()

con.close()
##------------------------------------------------------------------##
from sqlalchemy import create_engine
from sqlalchemy.sql import text

#We will connect to the MySQL database. We use a specific MySQL connection string.
eng = create_engine("mysql://testuser:test623@localhost/testdb")

with eng.connect() as con:

    con.execute(text('DROP TABLE IF EXISTS Cars'))
    con.execute(text('''CREATE TABLE Cars(Id INTEGER PRIMARY KEY, 
                 Name TEXT, Price INTEGER)'''))

    data = ( { "Id": 1, "Name": "Audi", "Price": 52642 },
             { "Id": 2, "Name": "Mercedes", "Price": 57127 },
             { "Id": 3, "Name": "Skoda", "Price": 9000 },
             { "Id": 4, "Name": "Volvo", "Price": 29000 },
             { "Id": 5, "Name": "Bentley", "Price": 350000 },
             { "Id": 6, "Name": "Citroen", "Price": 21000 },
             { "Id": 7, "Name": "Hummer", "Price": 41400 },
             { "Id": 8, "Name": "Volkswagen", "Price": 21600 }
    )

#Databases use different bind parameter constructs. With the text() function, we use a backend-neutral way to bind parameters.	
    for line in data:
        con.execute(text("""INSERT INTO Cars(Id, Name, Price) 
            VALUES(:Id, :Name, :Price)"""), **line)
##------------------------------------------------------------------##

##------------------------------------------------------------------##
#SQLAlchemy SQL Expression Language: 
'''
The SQLAlchemy Expression Language represents relational database structures and expressions using Python constructs. The expression language improves the maintainability of the code by hiding the SQL language and thus allowing not to mix Python code and SQL code.

The Object Relational Mapper, ORM, is built on top of the expression language.
'''
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select    
    
eng = create_engine('sqlite:///test.db')

with eng.connect() as con:

#We load the definition of the Cars table.
    meta = MetaData(eng)
    cars = Table('Cars', meta, autoload=True)  

#With the select() method, we create an SQL SELECT statement. This particular expression selects all columns and rows from the provided table.
    stm = select([cars])
    rs = con.execute(stm) 

    print rs.fetchall()
##------------------------------------------------------------------##
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select    
    
eng = create_engine('sqlite:///test.db')

with eng.connect() as con:

    meta = MetaData(eng)
    cars = Table('Cars', meta, autoload=True)  
#The limit() method limits the result set to three rows.
    stm = select([cars.c.Name, cars.c.Price]).limit(3)
    rs = con.execute(stm) 

    print rs.fetchall()
##------------------------------------------------------------------##
from sqlalchemy.sql import select, and_    
    
eng = create_engine('sqlite:///test.db')

with eng.connect() as con:

    meta = MetaData(eng)
    cars = Table('Cars', meta, autoload=True)  

#To build the expected SQL statement, we use the select() and where() methods and the and_() operator.
    stm = select([cars]).where(and_(cars.c.Price > 10000, cars.c.Price < 40000))
    rs = con.execute(stm) 

    print rs.fetchall()
##------------------------------------------------------------------##
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select    
    
eng = create_engine('sqlite:///test.db')

with eng.connect() as con:

    meta = MetaData(eng)
    cars = Table('Cars', meta, autoload=True)  

#With the like() method, we select all cars whose name ends with 'en'.
    stm = select([cars]).where(cars.c.Name.like('%en'))
    rs = con.execute(stm) 

    print rs.fetchall()
##------------------------------------------------------------------##
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, asc
    
eng = create_engine('sqlite:///test.db')

with eng.connect() as con:

    metadata = MetaData(eng)
    cars = Table('Cars', metadata, autoload=True)  

#The order_by() methos is given the asc() operator, which makes the ordering in ascending way.
    s = select([cars]).order_by(asc(cars.c.Name))
    rs = con.execute(s) 

    for row in rs:
        print row['Id'], row['Name'], row['Price']
##------------------------------------------------------------------##
from sqlalchemy import create_engine, Table, MetaData, tuple_
from sqlalchemy.sql import select
    
eng = create_engine('sqlite:///test.db')

with eng.connect() as con:

    meta = MetaData(eng)
    cars = Table('Cars', meta, autoload=True)  

#With the help of the tuple_() and in_() operators, we build the statement containing the IN clause.
    k = [(2,), (4,), (6,), (8,)]
    stm = select([cars]).where(tuple_(cars.c.Id).in_(k))
    rs = con.execute(stm) 

    for row in rs:
        print row['Id'], row['Name'], row['Price']
##------------------------------------------------------------------##
from sqlalchemy import (create_engine, Table, Column, Integer, 
    String, MetaData)
from sqlalchemy.sql import select    
    
eng = create_engine('sqlite:///:memory:')

with eng.connect() as con:

#We provide the definition of the table.
    meta = MetaData(eng)
    cars = Table('Cars', meta,
         Column('Id', Integer, primary_key=True),
         Column('Name', String),
         Column('Price', Integer)
    )
#The table is created using the create() method.
    cars.create()
#With the insert() method, we insert a new row into the table.
    ins1 = cars.insert().values(Id=1, Name='Audi', Price=52642)
    con.execute(ins1)

    ins2 = cars.insert().values(Id=2, Name='Mercedes', Price=57127)
    con.execute(ins2)
    
    ins3 = cars.insert().values(Id=3, Name='Skoda', Price=6000)
    con.execute(ins3)    

    s = select([cars])
    rs = con.execute(s) 

    for row in rs:
        print row['Id'], row['Name'], row['Price']
##------------------------------------------------------------------##
from sqlalchemy import (create_engine, Table, Column, Integer, String, ForeignKey, MetaData)
from sqlalchemy.sql import select    
    
eng = create_engine('sqlite:///test.db')

with eng.connect() as con:
    
    meta = MetaData(eng)
    
    authors = Table('Authors', meta, autoload=True)
    books = Table('Books', meta, autoload=True)

#The example executes an inner join on two tables
    stm = select([authors.join(books)])
    rs = con.execute(stm) 

    for row in rs:
        print row['Name'], row['Title']



##------------------------------------------------------------------##
'''
SQLAlchemy ORM:

SQLAlchemy consists of several components. Engine is the starting point of any SQLAlchemy application. The engine is an abstraction of the database and its API. It works with the connection pool and the Dialect component to deliver the SQL statements from the SQLAlchemy to the database. The engine is created using the create_engine() function. It can be used to directly interact with a database, or can be passed to a Session object to work with the object-relational mapper.

Dialect is the system SQLAlchemy uses to communicate with various types of DBAPI implementations and databases. All dialects require that an appropriate DBAPI driver is installed. SQLAlchemy has dialects for many popular database systems including Firebird, Informix, Microsoft SQL Server, MySQL, Oracle, PostgreSQL, SQLite, or Sybase. The Dialect is created from the supplied connection string.

MetaData comprises of Python objects that describe tables and other schema-level objects. Database metadata can be expressed by explicitly naming the various components and their properties, using constructs such as Table, Column, or ForeignKey. MetaData can be easily generated by SQLAlchemy using a process called reflection.

Inside the ORM, the primary interface for persistence operations is the Session. The Session establishes all conversations with the database and represents a container for all the objects which we have loaded or associated with it during its lifespan. It provides the entry point to acquire a Query object, which sends queries to the database using the Session object¡¯s current database connection, populating result rows into objects that are then stored in the Session.

When using ORM, we first configure database tables that we will be using. Then we define classes that will be mapped to them. Modern SQLAlchemy uses Declarative system to do these tasks. A declarative base class is created, which maintains a catalog of classes and tables. A declarative base class is created with the declarative_base() function.
After we have done the configurations, we create a session. A Session is the primary interface for persistence operations in the SQLAlchemy ORM. It establishes and maintains all conversations between our program and the database.
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

eng = create_engine('sqlite:///:memory:')

#A declarative base class is created with the declarative_base() function.
Base = declarative_base() 
 
#The user-defined Car class is mapped to the Cars table. The class inherits from the declarative base class.
class Car(Base): 
    __tablename__ = "Cars"
 
    Id = Column(Integer, primary_key=True)
    Name = Column(String)  
    Price = Column(Integer)

#The declarative Base is bound to the database engine.		
Base.metadata.bind = eng        
#The create_all() method creates all configured tables; in our case, there is only one table.
Base.metadata.create_all()        
        
#A session object is created.
Session = sessionmaker(bind=eng)
ses = Session()    

#With the add_all() method, we add the specified instances of Car classes to the session.
ses.add_all(
   [Car(Id=1, Name='Audi', Price=52642), 
    Car(Id=2, Name='Mercedes', Price=57127),
    Car(Id=3, Name='Skoda', Price=9000),
    Car(Id=4, Name='Volvo', Price=29000),
    Car(Id=5, Name='Bentley', Price=350000),
    Car(Id=6, Name='Citroen', Price=21000),
    Car(Id=7, Name='Hummer', Price=41400),
    Car(Id=8, Name='Volkswagen', Price=21600)])

#The changes are committed to the database with the commit() method.
ses.commit()

#The query() method loads all instances of the Car class and its all() method returns all results represented by the query as a list.
rs = ses.query(Car).all()

for car in rs:
    print car.Name, car.Price
##------------------------------------------------------------------##
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

eng = create_engine('sqlite:///test.db')

Base = declarative_base()
 
class Car(Base):
    __tablename__ = "Cars"
 
    Id = Column(Integer, primary_key=True)
    Name = Column(String)  
    Price = Column(Integer)
        
Session = sessionmaker(bind=eng)
ses = Session()    

c1 = Car(Name='Oldsmobile', Price=23450)
ses.add(c1)
ses.commit()

rs = ses.query(Car).all()

for car in rs:
    print car.Name, car.Price
##------------------------------------------------------------------##
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

eng = create_engine('sqlite:///test.db')

Base = declarative_base()
Base.metadata.bind = eng

class Car(Base):
    __tablename__ = "Cars"
 
    Id = Column(Integer, primary_key=True)
    Name = Column(String)  
    Price = Column(Integer)
            
Session = sessionmaker(bind=eng)
ses = Session()    

#The filter() method takes a filtering criterion, which is an [SQL expression object]. The criterion is created with the like() method.
rs = ses.query(Car).filter(Car.Name.like('%en'))

for car in rs:
    print car.Name, car.Price
##------------------------------------------------------------------##
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

eng = create_engine('sqlite:///test.db')

Base = declarative_base()
 
class Car(Base):
    __tablename__ = "Cars"
 
    Id = Column(Integer, primary_key=True)
    Name = Column(String)  
    Price = Column(Integer)
    
Session = sessionmaker(bind=eng)
ses = Session()    

#The filtering criterion is created by the in_() method. The method takes a list of Ids.
rs = ses.query(Car).filter(Car.Id.in_([2, 4, 6, 8]))

for car in rs:
    print car.Id, car.Name, car.Price
##------------------------------------------------------------------##
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

eng = create_engine('sqlite:///test.db')

Base = declarative_base()
 
#the author object will have a Books attribute.
class Author(Base):
    __tablename__ = "Authors"
 
    AuthorId = Column(Integer, primary_key=True)
    Name = Column(String)  
    Books = relationship("Book")

#A foreign key is defined by the ForeignKey type and the relationship() function.
#the book object will have a Author attribute.
class Book(Base):
    __tablename__ = "Books"
 
    BookId = Column(Integer, primary_key=True)
    Title = Column(String)      
    AuthorId = Column(Integer, ForeignKey("Authors.AuthorId"))    
                           
    Author = relationship("Author")                           
         
Session = sessionmaker(bind=eng)
ses = Session()   

res = ses.query(Author).filter(Author.Name=="Leo Tolstoy").first()

# retrieve foreignkey's object's DATA:
for book in res.Books:
    print book.Title

res = ses.query(Book).filter(Book.Title=="Emma").first()    
print res.Author.Name

##------------------------------------------------------------------##

##------------------------------------------------------------------##
#Schema Definition Lanuage:
'''
SQLAlchemy schema metadata is a comprehensive system of describing and inspecting database schemas. The core of SQLAlchemy's query and object mapping operations is supported by database metadata.
Metadata is information about the data in the database; for instance information about the tables and columns, in which we store data.
'''
from sqlalchemy import (create_engine, Table, Column, Integer, 
    String, MetaData)
    
meta = MetaData()
cars = Table('Cars', meta,
     Column('Id', Integer, primary_key=True),
     Column('Name', String),
     Column('Price', Integer)
)

print "The Name column:"
print cars.columns.Name
print cars.c.Name

print "Columns: "
for col in cars.c:
    print col
    
print "Primary keys:"
for pk in cars.primary_key:
    print pk    

print "The Id column:"
print cars.c.Id.name
print cars.c.Id.type
print cars.c.Id.nullable
print cars.c.Id.primary_key























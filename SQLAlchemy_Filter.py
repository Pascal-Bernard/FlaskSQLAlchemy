#----------------------------------------------------------------------------------------------------#
filter_by() + filter()
#----------------------------------------------------------------------------------------------------#

and filtering results, which is accomplished either with filter_by(), which uses keyword arguments:

SQL>>> for name, in session.query(User.name).\
...             filter_by(fullname='Ed Jones'):
...    print(name)
ed
...or filter(), which uses more flexible SQL expression language constructs. These allow you to use regular Python operators with the class-level attributes on your mapped class:

SQL>>> for name, in session.query(User.name).\
...             filter(User.fullname=='Ed Jones'):
...    print(name)
ed
The Query object is fully generative, meaning that most method calls return a new Query object upon which further criteria may be added. For example, to query for users named ¡°ed¡± with a full name of ¡°Ed Jones¡±, you can call filter() twice, which joins criteria using AND:

SQL>>> for user in session.query(User).\
...          filter(User.name=='ed').\
...          filter(User.fullname=='Ed Jones'):
...    print(user)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>
Common Filter Operators

Here¡¯s a rundown of some of the most common operators used in filter():

equals:

query.filter(User.name == 'ed')
not equals:

query.filter(User.name != 'ed')
LIKE:

query.filter(User.name.like('%ed%'))
IN:

query.filter(User.name.in_(['ed', 'wendy', 'jack']))

# works with query objects too:
query.filter(User.name.in_(
        session.query(User.name).filter(User.name.like('%ed%'))
))
NOT IN:

query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
IS NULL:

query.filter(User.name == None)

# alternatively, if pep8/linters are a concern
query.filter(User.name.is_(None))
IS NOT NULL:

query.filter(User.name != None)

# alternatively, if pep8/linters are a concern
query.filter(User.name.isnot(None))
AND:

# use and_()
from sqlalchemy import and_
query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))

# or send multiple expressions to .filter()
query.filter(User.name == 'ed', User.fullname == 'Ed Jones')

# or chain multiple filter()/filter_by() calls
query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')
Note

Make sure you use and_() and not the Python and operator!

OR:

from sqlalchemy import or_
query.filter(or_(User.name == 'ed', User.name == 'wendy'))
Note

Make sure you use or_() and not the Python or operator!

MATCH:

query.filter(User.name.match('wendy'))
Note

match() uses a database-specific MATCH or CONTAINS function; its behavior will vary by backend and is not available on some backends such as SQLite.


#----------------------------------------------------------------------------------------------------#
Using Textual SQL:

>>> session.query(User).filter(text("id<:value and name=:name")).\
...     params(value=224, name='fred').order_by(User.id).one()
<User(name='fred', fullname='Fred Flinstone', password='blah')>

>>> session.query(User).from_statement(
...                     text("SELECT * FROM users where name=:name")).\
...                     params(name='ed').all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>]

>>> stmt = text("SELECT name, id, fullname, password "
...             "FROM users where name=:name")
>>> stmt = stmt.columns(User.name, User.id, User.fullname, User.password)
SQL>>> session.query(User).from_statement(stmt).params(name='ed').all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>]

#----------------------------------------------------------------------------------------------------#
SQLAlchemy support JOIN operations but Django not??
#----------------------------------------------------------------------------------------------------#














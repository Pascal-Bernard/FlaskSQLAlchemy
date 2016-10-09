

'''
A connection pool is a standard technique used to maintain long running connections in memory for efficient 
re-use, as well as to provide management for the total number of connections an application might 
use simultaneously.
'''


# SQLAlchemy maintains a connection pool inside Session.
# you don't need to worry about Session pool, just get/use Session. right?? 

# http://docs.sqlalchemy.org/en/latest/core/pooling.html

'''
SQLAlchemy Connection Pooling ==>

A connection pool is a standard technique used to maintain long running connections in memory for efficient re-use, as well as to provide management for the total number of connections an application might use simultaneously.

Particularly for server-side web applications, a connection pool is the standard way to maintain a ¡°pool¡± of active database connections in memory which are reused across requests.

SQLAlchemy includes several connection pool implementations which integrate with the Engine. They can also be used directly for applications that want to add pooling to an otherwise plain DBAPI approach.

Connection Pool Configuration

The Engine returned by the create_engine() function in most cases has a QueuePool integrated, pre-configured with reasonable pooling defaults. If you¡¯re reading this section only to learn how to enable pooling - congratulations! You¡¯re already done.

The most common QueuePool tuning parameters can be passed directly to create_engine() as keyword arguments: pool_size, max_overflow, pool_recycle and pool_timeout. For example:

engine = create_engine('postgresql://me@localhost/mydb',
                       pool_size=20, max_overflow=0)
In the case of SQLite, the SingletonThreadPool or NullPool are selected by the dialect to provide greater compatibility with SQLite¡¯s threading and locking model, as well as to provide a reasonable default behavior to SQLite ¡°memory¡± databases, which maintain their entire dataset within the scope of a single connection.

All SQLAlchemy pool implementations have in common that none of them ¡°pre create¡± connections - all implementations wait until first use before creating a connection. At that point, if no additional concurrent checkout requests for more connections are made, no additional connections are created. This is why it¡¯s perfectly fine for create_engine() to default to using a QueuePool of size five without regard to whether or not the application really needs five connections queued up - the pool would only grow to that size if the application actually used five connections concurrently, in which case the usage of a small pool is an entirely appropriate default behavior.

Switching Pool Implementations

The usual way to use a different kind of pool with create_engine() is to use the poolclass argument. This argument accepts a class imported from the sqlalchemy.pool module, and handles the details of building the pool for you. Common options include specifying QueuePool with SQLite:

from sqlalchemy.pool import QueuePool
engine = create_engine('sqlite:///file.db', poolclass=QueuePool)
Disabling pooling using NullPool:

from sqlalchemy.pool import NullPool
engine = create_engine(
          'postgresql+psycopg2://scott:tiger@localhost/test',
          poolclass=NullPool)
Using a Custom Connection Function

All Pool classes accept an argument creator which is a callable that creates a new connection. create_engine() accepts this function to pass onto the pool via an argument of the same name:

import sqlalchemy.pool as pool
import psycopg2

def getconn():
    c = psycopg2.connect(username='ed', host='127.0.0.1', dbname='test')
    # do things with 'c' to set up
    return c

engine = create_engine('postgresql+psycopg2://', creator=getconn)
For most ¡°initialize on connection¡± routines, it¡¯s more convenient to use the PoolEvents event hooks, so that the usual URL argument to create_engine() is still usable. creator is there as a last resort for when a DBAPI has some form of connect that is not at all supported by SQLAlchemy.

Constructing a Pool

To use a Pool by itself, the creator function is the only argument that¡¯s required and is passed first, followed by any additional options:

import sqlalchemy.pool as pool
import psycopg2

def getconn():
    c = psycopg2.connect(username='ed', host='127.0.0.1', dbname='test')
    return c

mypool = pool.QueuePool(getconn, max_overflow=10, pool_size=5)
DBAPI connections can then be procured from the pool using the Pool.connect() function. The return value of this method is a DBAPI connection that¡¯s contained within a transparent proxy:

# get a connection
conn = mypool.connect()

# use it
cursor = conn.cursor()
cursor.execute("select foo")
The purpose of the transparent proxy is to intercept the close() call, such that instead of the DBAPI connection being closed, it is returned to the pool:

# "close" the connection.  Returns
# it to the pool.
conn.close()
The proxy also returns its contained DBAPI connection to the pool when it is garbage collected, though it¡¯s not deterministic in Python that this occurs immediately (though it is typical with cPython).

The close() step also performs the important step of calling the rollback() method of the DBAPI connection. This is so that any existing transaction on the connection is removed, not only ensuring that no existing state remains on next usage, but also so that table and row locks are released as well as that any isolated data snapshots are removed. This behavior can be disabled using the reset_on_return option of Pool.

A particular pre-created Pool can be shared with one or more engines by passing it to the pool argument of create_engine():

e = create_engine('postgresql://', pool=mypool)
Pool Events

Connection pools support an event interface that allows hooks to execute upon first connect, upon each new connection, and upon checkout and checkin of connections. See PoolEvents for details.

Dealing with Disconnects

The connection pool has the ability to refresh individual connections as well as its entire set of connections, setting the previously pooled connections as ¡°invalid¡±. A common use case is allow the connection pool to gracefully recover when the database server has been restarted, and all previously established connections are no longer functional. There are two approaches to this.

Disconnect Handling - Optimistic

The most common approach is to let SQLAlchemy handle disconnects as they occur, at which point the pool is refreshed. This assumes the Pool is used in conjunction with a Engine. The Engine has logic which can detect disconnection events and refresh the pool automatically.

When the Connection attempts to use a DBAPI connection, and an exception is raised that corresponds to a ¡°disconnect¡± event, the connection is invalidated. The Connection then calls the Pool.recreate() method, effectively invalidating all connections not currently checked out so that they are replaced with new ones upon next checkout:

from sqlalchemy import create_engine, exc
e = create_engine(...)
c = e.connect()

try:
    # suppose the database has been restarted.
    c.execute("SELECT * FROM table")
    c.close()
except exc.DBAPIError, e:
    # an exception is raised, Connection is invalidated.
    if e.connection_invalidated:
        print("Connection was invalidated!")

# after the invalidate event, a new connection
# starts with a new Pool
c = e.connect()
c.execute("SELECT * FROM table")
The above example illustrates that no special intervention is needed, the pool continues normally after a disconnection event is detected. However, an exception is raised. In a typical web application using an ORM Session, the above condition would correspond to a single request failing with a 500 error, then the web application continuing normally beyond that. Hence the approach is ¡°optimistic¡± in that frequent database restarts are not anticipated.

Setting Pool Recycle

An additional setting that can augment the ¡°optimistic¡± approach is to set the pool recycle parameter. This parameter prevents the pool from using a particular connection that has passed a certain age, and is appropriate for database backends such as MySQL that automatically close connections that have been stale after a particular period of time:

from sqlalchemy import create_engine
e = create_engine("mysql://scott:tiger@localhost/test", pool_recycle=3600)
Above, any DBAPI connection that has been open for more than one hour will be invalidated and replaced, upon next checkout. Note that the invalidation only occurs during checkout - not on any connections that are held in a checked out state. pool_recycle is a function of the Pool itself, independent of whether or not an Engine is in use.

Disconnect Handling - Pessimistic

At the expense of some extra SQL emitted for each connection checked out from the pool, a ¡°ping¡± operation established by a checkout event handler can detect an invalid connection before it is used. In modern SQLAlchemy, the best way to do this is to make use of the ConnectionEvents.engine_connect() event, assuming the use of a Engine and not just a raw Pool object:

from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select

some_engine = create_engine(...)

@event.listens_for(some_engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return

    # turn off "close with result".  This flag is only used with
    # "connectionless" execution, otherwise will be False in any case
    save_should_close_with_result = connection.should_close_with_result
    connection.should_close_with_result = False

    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select([1]))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select([1]))
        else:
            raise
    finally:
        # restore "close with result"
        connection.should_close_with_result = save_should_close_with_result
The above recipe has the advantage that we are making use of SQLAlchemy¡¯s facilities for detecting those DBAPI exceptions that are known to indicate a ¡°disconnect¡± situation, as well as the Engine object¡¯s ability to correctly invalidate the current connection pool when this condition occurs and allowing the current Connection to re-validate onto a new DBAPI connection.

For the much less common case of where a Pool is being used without an Engine, an older approach may be used as below:

from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy.pool import Pool

@event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
    except:
        # raise DisconnectionError - pool will try
        # connecting again up to three times before raising.
        raise exc.DisconnectionError()
    cursor.close()
Above, the Pool object specifically catches DisconnectionError and attempts to create a new DBAPI connection, up to three times, before giving up and then raising InvalidRequestError, failing the connection. The disadvantage of the above approach is that we don¡¯t have any easy way of determining if the exception raised is in fact a ¡°disconnect¡± situation, since there is no Engine or Dialect in play, and also the above error would occur individually for all stale connections still in the pool.

More on Invalidation

The Pool provides ¡°connection invalidation¡± services which allow both explicit invalidation of a connection as well as automatic invalidation in response to conditions that are determined to render a connection unusable.

¡°Invalidation¡± means that a particular DBAPI connection is removed from the pool and discarded. The .close() method is called on this connection if it is not clear that the connection itself might not be closed, however if this method fails, the exception is logged but the operation still proceeds.

When using a Engine, the Connection.invalidate() method is the usual entrypoint to explicit invalidation. Other conditions by which a DBAPI connection might be invalidated include:

a DBAPI exception such as OperationalError, raised when a method like connection.execute() is called, is detected as indicating a so-called ¡°disconnect¡± condition. As the Python DBAPI provides no standard system for determining the nature of an exception, all SQLAlchemy dialects include a system called is_disconnect() which will examine the contents of an exception object, including the string message and any potential error codes included with it, in order to determine if this exception indicates that the connection is no longer usable. If this is the case, the _ConnectionFairy.invalidate() method is called and the DBAPI connection is then discarded.
When the connection is returned to the pool, and calling the connection.rollback() or connection.commit() methods, as dictated by the pool¡¯s ¡°reset on return¡± behavior, throws an exception. A final attempt at calling .close() on the connection will be made, and it is then discarded.
When a listener implementing PoolEvents.checkout() raises the DisconnectionError exception, indicating that the connection won¡¯t be usable and a new connection attempt needs to be made.
All invalidations which occur will invoke the PoolEvents.invalidate() event.

Using Connection Pools with Multiprocessing

It¡¯s critical that when using a connection pool, and by extension when using an Engine created via create_engine(), that the pooled connections are not shared to a forked process. TCP connections are represented as file descriptors, which usually work across process boundaries, meaning this will cause concurrent access to the file descriptor on behalf of two or more entirely independent Python interpreter states.

There are two approaches to dealing with this.

The first is, either create a new Engine within the child process, or upon an existing Engine, call Engine.dispose() before the child process uses any connections. This will remove all existing connections from the pool so that it makes all new ones. Below is a simple version using multiprocessing.Process, but this idea should be adapted to the style of forking in use:

eng = create_engine("...")

def run_in_process():
  eng.dispose()

  with eng.connect() as conn:
      conn.execute("...")

p = Process(target=run_in_process)
The next approach is to instrument the Pool itself with events so that connections are automatically invalidated in the subprocess. This is a little more magical but probably more foolproof:

from sqlalchemy import event
from sqlalchemy import exc
import os

eng = create_engine("...")

@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    connection_record.info['pid'] = os.getpid()

@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    pid = os.getpid()
    if connection_record.info['pid'] != pid:
        connection_record.connection = connection_proxy.connection = None
        raise exc.DisconnectionError(
                "Connection record belongs to pid %s, "
                "attempting to check out in pid %s" %
                (connection_record.info['pid'], pid)
        )
Above, we use an approach similar to that described in Disconnect Handling - Pessimistic to treat a DBAPI connection that originated in a different parent process as an ¡°invalid¡± connection, coercing the pool to recycle the connection record to make a new connection.
'''




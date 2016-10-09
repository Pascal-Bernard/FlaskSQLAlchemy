

'''
A connection pool is a standard technique used to maintain long running connections in memory for efficient 
re-use, as well as to provide management for the total number of connections an application might 
use simultaneously.
'''


# SQLAlchemy maintains a connection pool inside Session.
# you don't need to worry about Session pool, just get/use Session. right?? 
# # -*- coding: utf-8 -*-
import os

# MYSQL_HOST = "10.240.212.140"
# MYSQL_USER = "bmcp"
# MYSQL_PWD = "bmcp"
# MYSQL_DB = "bmcp"
# MYSQL_PORT = 3306

# Config = {
#     "mysql": {
#         "connection": 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
#     },
#     "white_list": ['localhost'],
# }

path = os.path.abspath('.')
Config = {
    "sqlite": {
        "connection": 'sqlite:///%s/sqlite.db' % path
    },
    "white_list": ['localhost'],
}

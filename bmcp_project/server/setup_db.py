# -*- coding: utf-8 -*-
from server.db import Base, engine
from server.db.models import Test
from server.db import db_adapter
from server.utils import log


def setup_db():
    log.debug('set up db...')
    """Initialize db tables

    make sure db and user correctly created in mysql
    in case upgrade the table structure, the origin table need be dropped firstly
    """
    Base.metadata.create_all(bind=engine)

    # test add data into db
    db_adapter.add_object_kwargs(Test, name='test')

setup_db()

# -*- coding: utf-8 -*-

import json
from . import Base, db_adapter
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text, TypeDecorator
from sqlalchemy.orm import relation, backref


def relationship(*arg, **kw):
    ret = relation(*arg, **kw)
    db_adapter.commit()
    return ret


def to_dic(inst, cls):
    # add your covert method for things like datetime from db-type to python-type
    # and what-not that aren't serializable.
    convert = dict()
    # convert[TZDateTime] = date_serializer
    convert[DateTime] = str

    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type.__class__ in convert.keys() and v is not None:
            try:
                func = convert[c.type.__class__]
                d[c.name] = func(v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type.__class__])
        else:
            d[c.name] = v
    return d


def to_json(inst, cls):
    return json.dumps(to_dic(inst, cls))


class DBBase(Base):
    """
    DB model base class, providing basic functions
    """
    __abstract__ = True

    def __init__(self, **kwargs):
        super(DBBase, self).__init__(**kwargs)

    def dic(self):
        return to_dic(self, self.__class__)

    def json(self):
        return to_json(self, self.__class__)

    def __repr__(self):
        return '%s: %s' % (self.__class__.__name__, self.json())

"""
in manay-to-many relation, create a middle-table yourself and use [ForeignKey] from it link to other 2 tables.
so obviously just use the [ForeignKey] is enough for your develop.
"""


class Test(DBBase):
    __tablename__ = 'test_db'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Xclarity(DBBase):
    __tablename__ = 'xclarity'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    ipaddress = Column(String(255))
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    link = Column(String(255))
    state = Column(String(64))
    create_time = Column(DateTime)


class Server(DBBase):
    __tablename__ = 'physical_server'

    id = Column(String(64), primary_key=True)
    host_name = Column(String(50), unique=True, nullable=False)
    uuid = Column(String(255))
    ip_address = Column(String(39))
    mac_address = Column(String(64))
    status = Column(String(50))


class ServerMonitor(DBBase):
    __tablename__ = 'server_monitor'

    id = Column(Integer, primary_key=True)
    server_id = Column(String(64), ForeignKey(Server.id))
    time = Column(DateTime)
    level = Column(String(16))
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    processor_temperature = Column(Float)
    system_input_power = Column(Integer)
    system_output_power = Column(Integer)
    imm_status = Column(String(16))
    remark = Column(String(255))


class MonitorStrategy(DBBase):
    __tablename__ = 'monitor_strategy'

    id = Column(Integer, primary_key=True)
    server_id = Column(String(64), ForeignKey(Server.id))
    cpu_threshold = Column(Float)
    memory_threshold = Column(Float)
    disk_threshold = Column(Float)
    temperature_threshold = Column(Float)
    system_input_power_threshold = Column(Integer)
    system_output_power_threshold = Column(Integer)


class DeployEvent(DBBase):
    __tablename__ = 'deploy_event'

    id = Column(Integer, primary_key=True)
    server_id = Column(String(64), ForeignKey(Server.id))

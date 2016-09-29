# -*- coding: utf-8 -*-

__author__ = 'hubian'


class SERVER_STATUS:
    OK = 'ok'
    WARNING = 'warning'
    ERROR = 'error'


class SERVER_MONITOR_LEVEL:
    NORMAL = 'normal'
    WARNING = 'warning'
    ERROR = 'error'


class SERVER_POWER:
    ON = 'On'
    OFF = 'Off'


class SERVER_DEPLOY_SERVICE:
    NOVA = 'openstack-nova'
    HORIZON = 'openstack-horizon'
    UBUNTU = 'ubuntu-server'


class IMM_STATUS:
    ONLINE = 'online'
    OFFLINE = 'offline'

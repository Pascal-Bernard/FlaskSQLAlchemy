# -*- coding: utf-8 -*-

from server import api
from server.db import db_adapter
from server.db.models import Server, ServerMonitor
from flask_restful import Resource, reqparse
from flask import request
from datetime import datetime
from server.physical_server import server_manager
from server.utils import utils
from server.xclarity import xclarity_manager
from server.monitor_strategy import monitor_strategy_manager


class TestResource(Resource):
    def get(self):
        return "server started"


class HostResource(Resource):
    def get(self):
        return db_adapter.find_first_object_by(Server, id=1).dic()


class XclarityResource(Resource):
    def post(self):
        xclarity_info = request.get_json(force=True)
        xclarity_manager.add_xclarity(xclarity_info)

    def delete(self):
        parse = reqparse.RequestParser()
        parse.add_argument('id', type=int, location='args', required=True)
        args = parse.parse_args()
        xclarity_manager.delete_xclarity(args['id'])


class XclarityListResource(Resource):
    def get(self):
        xclarity_list = map(lambda xclarity: xclarity.dic(), xclarity_manager.get_xclarity_list())
        return {'data': xclarity_list}


class MonitorStrategyResource(Resource):
    def post(self, server_id):
        monitor_strategy_info = request.get_json(force=True)
        monitor_strategy_manager.add_monitor_strategy(server_id, monitor_strategy_info)

    def put(self, server_id):
        monitor_strategy_info = request.get_json(force=True)
        monitor_strategy_manager.update_monitor_strategy(monitor_strategy_info)

    def delete(self, server_id):
        parse = reqparse.RequestParser()
        parse.add_argument('id', type=int, location='args', required=True)
        args = parse.parse_args()
        monitor_strategy_manager.delete_monitor_strategy(args['id'])


class ServerListResource(Resource):
    def get(self):
        # take filters into consideration
        parse = reqparse.RequestParser()
        parse.add_argument('status', type=str, location='args')
        parse.add_argument('power', type=str, location='args')
        args = parse.parse_args()
        return map(lambda server: server.dic(), server_manager.get_server_list(args))


class ServerResource(Resource):
    def get(self):
        # get details info
        parse = reqparse.RequestParser()
        parse.add_argument('id', type=int, location='args', required=True)
        args = parse.parse_args()
        return server_manager.get_server_details(args['id'])


class ServerSummaryResource(Resource):
    def get(self):
        return {
            'data': {
                'power_on': db_adapter.count_by(Server, power_status='on'),
                'power_off': db_adapter.count_by(Server, power_status='off'),
                'power_unknown': db_adapter.count_by(Server, power_status='unknown'),
                'ok': db_adapter.count_by(Server, monitor_status='ok'),
                'warning': db_adapter.count_by(Server, monitor_status='warning'),
                'error': db_adapter.count_by(Server, monitor_status='error'),
                'unknown': db_adapter.count_by(Server, monitor_status='unknown')
            }
        }


class ServerMonitorResource(Resource):
    def get(self, server_id):
        # get the server's last monitor data record in db
        return {'data': monitor_strategy_manager.get_server_lastest_monitor_data(server_id)}


class ServerHistoryMonitorResource(Resource):
    def get(self, server_id, tag):
        date = utils.get_now()
        time = datetime(date.year, date.month, date.day)
        if tag == "CurrentDay":
            history_monitor_list = db_adapter.find_all_objects(ServerMonitor,
                                                               ServerMonitor.server_id == server_id,
                                                               ServerMonitor.time >= time)
        else:
            history_monitor_list = db_adapter.find_all_objects(ServerMonitor,
                                                               ServerMonitor.server_id == server_id)
        return history_monitor_list


def init_routes():
    api.add_resource(TestResource, "/api/test")
    api.add_resource(HostResource, "/api/servers")

    api.add_resource(XclarityResource, "/api/xclarity")
    api.add_resource(XclarityListResource, "/api/xclarity/list")

    api.add_resource(MonitorStrategyResource, "/api/server/<int:server_id>/monitorStrategy")

    api.add_resource(ServerListResource, "/api/server/list")
    api.add_resource(ServerSummaryResource, "/api/server/summary")
    api.add_resource(ServerResource, "/api/server")
    api.add_resource(ServerMonitorResource, "/api/server/<int:server_id>/monitor")
    api.add_resource(ServerHistoryMonitorResource, "/api/server/<int:server_id>/historyMonitor/<string:tag>")

from server.db import db_adapter
from server.db.models import Server
from server.db.models import ServerMonitor
from server.monitor_strategy import monitor_strategy_manager

class ServerManagemer:
    def inventory_servers(self, xclarity_id):
        pass

    def update_server(self, server_id, **kwargs):
        pass

    def get_server_details(self, server_id):
        server = db_adapter.find_all_objects_by(ServerMonitor, id=server_id).dic()
        server_strategy = monitor_strategy_manager.get_server_strategy(server_id)
        lastest_server_monitor_data = monitor_strategy_manager.get_server_lastest_monitor_data(server_id)

        return {
            'data': {
                'server': server,
                'server_monitor_data': lastest_server_monitor_data,
                'server_strategy': server_strategy
            }
        }

    def get_server_list(self, args):
        condition = 1 == 1
        if 'status' in args:
            condition = condition and (Server.status == args['status'])
        if 'power' in args:
            condition = condition and (Server.power_status == args['status'])
        server_list = db_adapter.find_all_objects(Server, condition)
        return server_list

    def server_assign(self, server_id, username):
        pass

    def __insert_server_from_parsing_physical_server_info(self, physical_server_info):
        pass

from server.monitor_strategy import monitor_strategy_manager
from server.db import db_adapter
from server.xclarity import xclarity_manager
from server.db.models import Server, ServerMonitor
from server.utils import utils


def sync_servers_info():
    """
    node info collection and sync into DB
    all xclarity's all Physical Servers will be take into consideration
    """

    server_list = db_adapter.find_all_object(Server)

    for server in server_list:
        xclarity_connection = xclarity_manager.get_xclarity_connection(server.xclarity_id)
        monitor_info = xclarity_connection.get_server_monitor_info(server.uuid, server.imm_ip)
        monitor_level, message = monitor_strategy_manager.get_level_from_monitor_info(server.id, monitor_info)
        monitor_value = ServerMonitor(server_id=server.id,
                                      time=utils.get_now(),
                                      level=monitor_level,
                                      cpu_usage=monitor_info['cpu_usage'],
                                      memory_usage=monitor_info['memory_usage'],
                                      disk_usage=monitor_info['disk_usage'],
                                      processor_temperature=monitor_info['processor_remperature'],
                                      system_input_power=monitor_info['system_input_power'],
                                      system_output_power=monitor_info['system_out_power'],
                                      imm_status=monitor_info['imm_status'],
                                      remark=message)
        db_adapter.add_object(monitor_value)

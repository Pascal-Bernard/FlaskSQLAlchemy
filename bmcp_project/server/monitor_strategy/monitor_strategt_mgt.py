from server.utils import log
from server.db import db_adapter
from server.db.models import ServerMonitor, MonitorStrategy
from server.utils.constants import SERVER_MONITOR_LEVEL, IMM_STATUS
from sqlalchemy import desc


class MonitorStrategyManager:
    def add_monitor_strategy(self, server_id, strategy_info):
        try:
            db_adapter.add_object_kwargs(MonitorStrategy,
                                         cpu_threshold=strategy_info['cpu_threshold'],
                                         memory_threshold=strategy_info['memory_threshold'],
                                         disk_threshold=strategy_info['disk_threshold'],
                                         temperature_threshold=strategy_info['temperature_threshold'],
                                         system_input_power_threshold=strategy_info['system_input_power_threshold'],
                                         system_output_power_threshold=strategy_info['system_output_power_threshold'],
                                         server_id=server_id)
        except Exception as ex:
            log.error("MonitorStrategy creation failed, details error info")
            log.error(ex)

    def get_server_strategy(self, server_id):
        return db_adapter.find_first_object_by(MonitorStrategy, server_id=server_id).dic()

    def update_monitor_strategy(self, monitor_strategy_info):
        monitor_strategy_db = db_adapter.get_object(MonitorStrategy, monitor_strategy_info['id'])
        update_info = dict(monitor_strategy_info.viewitems() - monitor_strategy_db.dic().viewitems())
        db_adapter.update_object(monitor_strategy_db, **update_info)

    def delete_monitor_strategy(self, monitor_strategy_id):
        db_adapter.delete_all_objects_by(MonitorStrategy, id=monitor_strategy_id)

    def get_level_from_monitor_info(self, server_id, monitor_info):
        strategy_value = self.get_server_strategy(server_id)
        message = "//%s exceeded"
        warn_message = SERVER_MONITOR_LEVEL.WARNING

        if monitor_info['cpu_usage'] >= strategy_value['cpu_threshold']:
            warn_message += message % 'cpu_usage'
        elif monitor_info['memory_usage'] >= strategy_value['memory_threshold']:
            warn_message += message % 'memory_usage'
        elif monitor_info['disk_usage'] >= strategy_value['disk_threshold']:
            warn_message += message % 'disk_usage'
        elif monitor_info['temperature_usage'] >= strategy_value['temperature_threshold']:
            warn_message += message % 'temperature_usage'
        elif monitor_info['system_input_power'] >= strategy_value['system_input_power']:
            warn_message += message % 'system_input_power'
        elif monitor_info['system_output_power'] >= strategy_value['system_output_power']:
            warn_message += message % 'system_output_power'
        elif monitor_info['imm_status'] == IMM_STATUS.OFFLINE:
            warn_message += "//The IMM server is offline"

        if warn_message != SERVER_MONITOR_LEVEL.WARNING:
            return SERVER_MONITOR_LEVEL.WARNING, warn_message
        else:
            return SERVER_MONITOR_LEVEL.NORMAL, SERVER_MONITOR_LEVEL.NORMAL

    def get_server_lastest_monitor_data(self, server_id):
        server_monitor = db_adapter.find_all_objects_order_by(ServerMonitor,
                                                              1,
                                                              desc(ServerMonitor.time),
                                                              id=server_id).dic()
        return server_monitor

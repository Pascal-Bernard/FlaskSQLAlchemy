from server.db import db_adapter
from server.db.models import Xclarity
from server.utils import utils, log
from server.xclarity import xclarity_adapter


class XclarityManager:
    xclarity_instance = {}

    def get_xclarity_connection(self, xclarity_id):
        if xclarity_id in self.xclarity_instance:
            return self.xclarity_instance[xclarity_id]
        else:
            xclarity_info = self.get_xclarity_list(id=xclarity_id)
            xclarity_connection = xclarity_adapter.get_xclarity_connection('',
                                                                           xclarity_info.ipaddress,
                                                                           xclarity_info.username,
                                                                           xclarity_info.password)

            self.xclarity_instance[xclarity_id] = xclarity_connection
            return xclarity_connection

    def add_xclarity(self, xclarity_info):
        try:
            db_adapter.add_object_kwargs(Xclarity,
                                         name=xclarity_info['Name'],
                                         ipaddress=xclarity_info['IPAddress'],
                                         username=xclarity_info['User'],
                                         password=xclarity_info['Password'],
                                         link=xclarity_info['Link'],
                                         state=xclarity_info['State'],
                                         create_time=utils.get_now())
        except Exception as ex:
            log.error("XClarity creation failed, details error info")
            log.error(ex)

    def delete_xclarity(self, xclarity_id):
        db_adapter.delete_all_objects_by(Xclarity, id=xclarity_id)

    def get_xclarity_list(self, **kwargs):
        return db_adapter.find_all_objects(Xclarity, **kwargs)

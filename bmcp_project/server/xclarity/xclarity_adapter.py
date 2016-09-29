# -*- coding: utf-8 -*-

from __future__ import division
import requests
import json
from server.utils import log, exception
from server.utils.constants import IMM_STATUS

"""
xclarity wrapper to execute all the xclarity operations
"""


def get_xclarity_connection(context, ip, user, passwd):
    """
    get the xclarity connection by detail info
    """
    log.info('get the xclarity connection')
    xclarity_api = XClarityAPI(context, ip, user, passwd)
    log.info('end of getting the xclarity connection')
    return xclarity_api


def get_xclarity_connection_by_node(context, node):
    """
    get the xclarity connection by node
    """
    driver_info = node.driver_info
    ip = driver_info.get('xclarity_ip')
    user = driver_info.get('xclarity_username')
    passwd = driver_info.get('xclarity_password')
    xclarity_api = XClarityAPI(context, ip, user, passwd)
    # log.warn('end of getting the xclarity connection by node')
    return xclarity_api


def _http_log_req(method, url, body=None, headers=None):
    log.debug("REQ:%(method)s %(url)s %(headers)s %(body)s\n",
              {'method': method,
               'url': url,
               'headers': headers,
               'body': body})


def _http_log_resp(resp, body):
    log.debug("RESP:%(code)s %(headers)s %(body)s\n",
              {'code': resp.status_code,
               'headers': resp.headers,
               'body': body})


class XClarityAPI(object):
    """
    Client for interacting with xClarity via a REST API.
    """

    def __init__(self, context, host, username, password, **kwargs):
        self.context = context
        self.host = host
        self.username = username
        self.password = password

        # Optional args
        self.scheme = kwargs.pop('scheme', 'https')
        self.port = kwargs.pop('port', 443)
        self.verify = kwargs.pop('verify', False)

    def _do_request(self, method, url, body=None, headers=None):
        # Connects to the server and issues a request.
        # :returns: result data
        # :raises: IOError if the request fails

        url = "%s://%s:%s%s" % (self.scheme, self.host, self.port, url)

        try:
            _http_log_req(method, url, body, headers)
            resp = requests.request(method, url, data=body,
                                    headers=headers, auth=(self.username, self.password),
                                    verify=self.verify)
            _http_log_resp(resp, resp.text)

            status_code = resp.status_code
            if status_code in (requests.codes.OK,
                               requests.codes.CREATED,
                               requests.codes.ACCEPTED,
                               requests.codes.NO_CONTENT):
                try:
                    """Deserializes an JSON string into a dictionary."""
                    return status_code, json.loads(resp.text)
                except (TypeError, ValueError):
                    return status_code, resp.text
            else:
                return self._handle_fault_response(status_code, resp)

        except requests.exceptions.ConnectionError as e:
            log.debug("throwing ConnectionFailed : %s", e)
            raise exception.XClarityConnectionFailed(explanation=e)

    def _handle_fault_response(self, status_code, resp):
        log.debug("Error message: %s", resp.text)

        try:
            error_body = json.loads(resp.text)
            if error_body:
                explanation = error_body['messages'][0]['explanation']
                recovery = error_body['messages'][0]['recovery']['text']
        except Exception:
            # If unable to deserialized body it is probably not a
            # xClarity error
            explanation = resp.text
            recovery = ''
        # Raise the appropriate exception
        kwargs = {'explanation': explanation, 'recovery': recovery}
        raise exception.XClarityInternalFault(**kwargs)

    def _validate_flexcat_json(self, data):
        if data['result'] == 'success':
            return

        try:
            explanation = data['messages'][0]['explanation']
            recovery = data['messages'][0]['recovery']['text']
        except Exception:
            # If unable to deserialized body it is probably not a
            # xClarity error
            explanation = data
            recovery = ''
        kwargs = {'explanation': explanation, 'recovery': recovery}
        raise exception.XClarityInternalFault(**kwargs)

    def list_os_images(self):
        status_code, data = self._do_request('GET', '/osImages')
        self._validate_flexcat_json(data)
        return data

    def list_managed_nodes(self):
        status_code, data = self._do_request('GET', '/nodes?status=managed')
        return data

    def get_one_managed_node(self, uuid):
        status_code, data = self._do_request('GET', '/nodes/%s?status=managed' % uuid)
        return data

    def list_host_platforms(self):
        status_code, data = self._do_request('GET', '/hostPlatforms')
        self._validate_flexcat_json(data)
        return data

    def get_host_platform(self, uuid):
        data = self.list_host_platforms()
        if data:
            for item in data['items']:
                if uuid == item['uuid']:
                    return item
        return None

    def get_global_settings(self):
        status_code, data = self._do_request('GET', '/osdeployment/globalSettings')
        return data

    def set_global_settings(self, ip_assignment):
        put_body = {
            'ipAssignment': ip_assignment,
        }
        put_body = json.dumps(put_body)
        status_code, data = self._do_request('PUT', '/osdeployment/globalSettings', body=put_body)
        return data

    def set_power_state(self, node_uuid, power_state):
        """
        Set the current power state.

        :param node_uuid: The xClarity Node UUID.
        :param power_state: The desired power state. Allowed values are
            'powerOn | powerOff | powerCycleSoft | powerCycleSoftGraceful | powerOffGraceful | powerNMI'.
        """
        log.warn('in xClarity service, set power state %(state)s for %(uuid)s',
                 {'state': power_state, 'uuid': node_uuid})
        put_body = {
            'powerState': power_state,
        }
        put_body = json.dumps(put_body)
        status_code, data = self._do_request('PUT', '/node/%s' % node_uuid, body=put_body)
        return data

    def get_power_state(self, node_uuid):
        """
        Set the current power state.

        :param node_uuid: The xClarity Node UUID.
        :param power_state: The desired power state. Allowed values are
            'powerOn | powerOff | powerCycleSoft | powerCycleSoftGraceful | powerOffGraceful | powerNMI'.
        """
        status_code, data = self._do_request('GET', '/nodes/%s?status=managed' % node_uuid)
        power_state = data.get('powerStatus', 'unknown')
        if power_state == 5:
            return 'power off'
        elif power_state == 8:
            return 'power on'
        else:
            return 'unknown'

    def get_fuelgauge(self):
        """
        Use this REST API to retrieve information about the processor usage, 
        memory usage, and disk capacity on the host system.
        """
        status_code, data = self._do_request('GET', '/fuelgauge')
        return data['response']

    def get_node_metrics(self, node_uuid):
        """
        return processor temperature and system power
        """
        status_code, data = self._do_request('GET', '/nodes/metrics/%s' % node_uuid)
        return data['energyMetrics']

    def get_physical_server_info(self, node_uuid):
        status_code, data = self._do_request('GET', '/nodes/%s' % node_uuid)
        # need improve
        return {'description': data['description'], 'host_name': data['hostname'],
                'ip_address': data['ipInterfaces'], 'leds': data['leds']['state'],
                'mac_address': data['macAddress'], 'machine_type': data['machineType'],
                'manufacturer': data['manufacturer'], 'model': data['model'],
                'part_number': data['partNumber'], 'serial_number': data['serialNumber'],
                'url': data['uri'], 'uuid': data['uuid'],
                'power_status': data['powerStatus'], 'management_ip': data['mgmtProcIPaddress'],
                'location': data['location']['location'], 'position_id': data['posID'],
                'imm_ip': data['ipInterfaces'], "status": data['accessState']
                }

    def get_imm_status(self, imm_ip):
        url = "http://%s/" % imm_ip
        try:
            resp = requests.get(url, timeout=2)
            if resp.status_code in (requests.codes.OK,
                                    requests.codes.CREATED,
                                    requests.codes.ACCEPTED,
                                    requests.codes.NO_CONTENT):
                return IMM_STATUS.ONLINE
            else:
                log.error("The IMM server is offline, the imm_ip is %s" % imm_ip)
                return IMM_STATUS.OFFLINE
        except Exception:
            log.error("The IMM server is offline, the imm_ip is %s" % imm_ip)
            return IMM_STATUS.OFFLINE

    def get_server_monitor_info(self, node_uuid, imm_ip):

        fuelgauge_info = self.get_fuelgauge()
        cpu_usage = fuelgauge_info['LoadAvg5Min']
        try:
            memory_usage = 100 * round((1 - fuelgauge_info['MemAvailable'] / fuelgauge_info['MemTotal']), 4)
        except ZeroDivisionError:
            log.error("The total memory capacity is zero, the node_uuid is %s." % node_uuid)
            memory_usage = 101

        partition_available = fuelgauge_info['sda1PartitionAvailable'] + \
                              fuelgauge_info['sda2PartitionAvailable'] + \
                              fuelgauge_info['sda3PartitionAvailable'] + \
                              fuelgauge_info['sda4PartitionAvailable']
        total_partition = fuelgauge_info['sda1PartitionTotal'] + \
                          fuelgauge_info['sda2PartitionTotal'] + \
                          fuelgauge_info['sda3PartitionTotal'] + \
                          fuelgauge_info['sda4PartitionTotal']
        try:
            disk_usage = 100 * round((1 - partition_available / total_partition), 4)
        except ZeroDivisionError:
            log.error("The total disk capacity is zero, the node_uuid is %s." % node_uuid)
            disk_usage = 101

        processor_info = self.get_node_metrics(node_uuid)
        imm_status = self.get_imm_status(imm_ip)
        server_info = {"cpu_usage": total_partition,
                       "memory_usage": memory_usage,
                       "disk_usage": disk_usage,
                       "processor_temperature": processor_info["inletAirTemperature"],
                       "system_input_power": processor_info["system_input_power"],
                       "system_output_power": processor_info["system_output_power"],
                       "imm_status": imm_status}
        return server_info

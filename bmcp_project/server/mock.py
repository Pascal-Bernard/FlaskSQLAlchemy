# -*- coding: utf-8 -*-
# __author__ = 'hubian'

from server import api
from flask_restful import Resource
import uuid


# for test
class Test(Resource):

    def get(self, ):
        return {
            "test": "it is a test"
        }


def get_members(element, url, total):
    members = []
    i = 0
    while i < total:
        dic = dict()
        dic["@odata.id"] = url + element + str(i + 1)
        members.append(dic)
        i += 1
    return members


def get_chassis():
    members1 = get_members("Rack", "/redfish/v1/Chassis/", 2)
    members2 = get_members("Chassis", "/redfish/v1/Chassis/", 3)
    members3 = get_members("Drawer", "/redfish/v1/Chassis/", 6)
    return members1 + members2 + members3


chassis_collection = get_chassis()


def get_volumes(element, url, total):
    members = []
    i = 0
    while i < total:
        dic = dict()
        dic["LUN"] = i + 1
        dic["Drive"] = url + element + str(i + 1)
        members.append(dic)
        i += 1
    return members


volume_collection = get_volumes(
    "volume", "/redfish/v1/Services/service1/LogicalDrives/", 12)


chassis_location2 = {'Chassis1': ['6 U', '10 U', 1], 'Chassis2': ['26 U', '10 U', 1], 'Chassis3': ['27 U', '10 U', 2], 'Drawer1': ['21 U', '2 U', 1], 'Drawer2': ['11 U', '2 U', 2], 'Drawer3': [
    '13 U', '2 U', 2], 'Drawer4': ['24 U', '1 U', 1], 'Drawer5': ['20 U', '1 U', 2], 'Drawer6': ['21 U', '1 U', 2], 'Rack1': ['0 U', '0 U', 1], 'Rack2': ['0 U', '0 U', 2]}


# /redfish/v1
class Redfishv1(Resource):

    def get(self):
        return {
            "@odata.context": "/redfish/v1/$metadata#ServiceRoot.ServiceRoot",
            "@odata.id": "/redfish/v1/",
            "@odata.type": "#ServiceRoot.1.0.0.ServiceRoot",
            "Id": "RootService",
            "Name": "Root Service",
            "RedfishVersion": "1.0.0",
            "UUID": "92384634-2938-2342-8820-489239905423",
            "Systems": {"@odata.id": "/redfish/v1/Systems"
                        },
            "Chassis": {
                "@odata.id": "/redfish/v1/Chassis"
            },
            "Managers": {
                "@odata.id": "/redfish/v1/Managers"
            },
            "EventService": {
                "@odata.id": "/redfish/v1/EventService"
            },
            "Services": {
                "@odata.id": "/redfish/v1/Services"
            },
            "EthernetSwitches": {
                "@odata.id": "/redfish/v1/EthernetSwitches"
            },
            "Oem": {
                "Intel:RackScale": {
                    "@odata.type": "#Intel.Oem.ServiceRoot",
                    "ApiVersion": "1.2.0",
                }
            },
            "Links": {}
        }


# /redfish/v1/Chassis
class Chassis(Resource):

    def get(self, ):
        return {
            "@odata.context": "/redfish/v1/$metadata#Chassis",
            "@odata.id": "/redfish/v1/Chassis",
            "@odata.type": "#ChassisCollection.ChassisCollection",
            "Name": "Chassis Collection",
            "Members@odata.count": 11,
            "Members": chassis_collection
        }


# /redfish/v1/Chassis/{chassis_id}
class ChassisDetail(Resource):

    def get(self, chassis_id):
        chassis_id = str(chassis_id)
        number = int(filter(str.isdigit, chassis_id))
        uuid_ = str(uuid.uuid3(uuid.NAMESPACE_DNS, chassis_id))
        manufacturer = 'Intel Corporaion'
        sku = uuid_[:13]
        asserttag = chassis_id
        serialnumber = uuid_[-12:]
        partnumber = uuid_[9:18]
        if 'Rack' in chassis_id and number <= 2:
            name = 'Rack%s' % number
            type_ = 'Rack'
            model = 'Intel RSA Chassis-Rack'
            contained = 'Rack' + str(number)
            managedby = number
            if number == 1:
                contains = chassis_collection[
                    2:4] + chassis_collection[5:6] + chassis_collection[8:9]
            else:
                contains = chassis_collection[
                    4:5] + chassis_collection[6:8] + chassis_collection[9:]
            computersystems = []
        elif 'Chassis' in chassis_id and number <= 5:
            name = 'FLEX-%s' % number
            type_ = 'Drawer'
            model = 'Lenovo FLEX 8731'
            contained = 'Rack1' if number <= 2 else 'Rack2'
            contains = [
                {"@odata.id": "/redfish/v1/Chassis/Chassis%d" % number}]
            num = (number - 1) * 14
            computersystems = get_members(
                "system", "/redfish/v1/Systems/", 48)[num:num + 14]
            managedby = number + 2
        else:
            name = 'ServerNode%s' % number
            type_ = 'Drawer'
            model = 'Lenovo System x3120'
            contained = 'Rack1' if number == 1 or number == 4 else 'Rack2'
            contains = [{"@odata.id": "/redfish/v1/Chassis/Drawer%d" % number}]
            num = number + 41
            computersystems = get_members(
                "system", "/redfish/v1/Systems/", 48)[num]
            managedby = number + 5
        return {
            "@odata.context": "/redfish/v1/$metadata#Chassis/Members/$entity",
            "@odata.id": "/redfish/v1/Chassis/" + chassis_id,
            "@odata.type": "#Chassis.1.0.0.Chassis",
            "Id": chassis_id,
            "ChassisType": type_,
            "Name": name,
            "Description": name,
            "Manufacturer": manufacturer,
            "Model": model,
            "SKU": sku,
            "SerialNumber": serialnumber,
            "PartNumber": partnumber,
            "AssetTag": asserttag,
            "IndicatorLED": "On",
            "Status": {
                "State": "Enabled",
                "Health": "OK",
                "HealthRollup": "OK"
            },
            "Oem": {
                "Lenovo:RackScale": {
                    "@odata.type": "#Intel.Oem.Chassis",
                    "Location": {
                        "Rack": "Rack" + str(chassis_location2[chassis_id][2]),
                        "ULocation": chassis_location2[chassis_id][0],
                        "UHeight": chassis_location2[chassis_id][1]
                    },
                    "UUID": uuid_
                }
            },
            "Links": {
                "Contains": contains,
                "ContainedBy": {
                    "@odata.id": "/redfish/v1/Chassis/%s" % contained
                },
                "ComputerSystems": computersystems,
                "Switches": [  # TODO
                    {
                        "@odata.id": "/redfish/v1/EthernetSwitches/switch1"
                    }
                ],
                "ManagedBy": [
                    {
                        "@odata.id": "/redfish/v1/Managers/manager%d" % managedby
                    }
                ],
                "ManagersIn": [
                    {
                        "@odata.id": "/redfish/v1/Managers/manager%d" % managedby  # managedby = managerin
                    }
                ],
                "Oem": {}
            }
        }


# /redfish/v1/Systems
class Systems(Resource):

    def get(self, ):
        members = get_members("system", "/redfish/v1/Systems/", 48)
        return {
            "@odata.context": "/redfish/v1/$metadata#ComputerSystemCollection.ComputerSystemCollection",
            "@odata.id": "/redfish/v1/Systems",
            "@odata.type": "#ComputerSystemCollection.ComputerSystemCollection",
            "Name": "Computer System Collection",
            "Members@odata.count": 48,
            "Members": members
        }


# /redfish/v1/Systems/{system_id}
class SystemDetail(Resource):

    def get(self, system_id):
        system_id = str(system_id)
        number = int(filter(str.isdigit, system_id))
        uuid_ = str(uuid.uuid3(uuid.NAMESPACE_DNS, system_id))
        sku = uuid_[:13]
        asserttag = 'asset tag%s' % system_id
        serialnumber = uuid_[-12:]
        partnumber = uuid_[9:18]
        manufacturer = 'Dual socket Xeon Server'
        if 43 <= number <= 48:
            type_ = 'Logical'
            name = 'ServerNode%s' % str(number - 42)
            description = 'Nova node%s' % str(number - 42)
            model = 'Lenovo System x3120' if number <= 45 else 'Lenovo System x3650'
            hostname = 'nova-%s' % str(number)
            chassis_id = 'Drawer%d' % (number - 42)
            managedby = number - 37
        else:
            type_ = 'Physical'
            name = 'LTE-%s' % str(number)
            description = 'Nova node%s' % str(number)
            model = 'Lenovo System x3120' if number <= 8 else 'Lenovo System x3650'
            hostname = 'nova-%s' % str(number)
            if 29 <= number:
                chassis_id = 'Chassis%d' % 3
                managedby = 5
            else:
                chassis_id = 'Chassis%d' % 2 if 15 <= number else 'Chassis%d' % 1
                managedby = 4 if 15 <= number else 3
        return {
            "@odata.context": "/redfish/v1/$metadata#Systems/Members/$entity",
            "@odata.id": "/redfish/v1/Systems/" + system_id,
            "@odata.type": "#ComputerSystem.1.0.0.ComputerSystem",
            "Id": system_id,
            "Name": name,
            "SystemType": type_,
            "AssetTag": asserttag,
            "Manufacturer": manufacturer,
            "Model": model,
            "SKU": sku,
            "SerialNumber": serialnumber,
            "PartNumber": partnumber,
            "Description": description,
            "UUID": uuid_,
            "HostName": hostname,
            "Status": {
                "State": "Enabled",
                "Health": "OK",
                "HealthRollUp": "OK"
            },
            "IndicatorLED": "On",
            "PowerState": "On",
            "Boot": {
                "BootSourceOverrideEnabled": "Once",
                "BootSourceOverrideTarget": "Pxe",
                "BootSourceOverrideTarget@Redfish.AllowableValues": ["None",
                                                                     "Pxe",
                                                                     "Hdd"],
            },
            "BiosVersion": "P79 v1.00 (09/20/2013)",
            "ProcessorSummary": {
                "Count": 8,
                "Model": "Multi-Core Intel(R) Xeon(R) processor 7xxx Series",
                "Status": {
                    "State": "Enabled",
                    "Health": "OK",
                    "HealthRollUp": "OK"
                }
            },
            "MemorySummary": {
                "TotalSystemMemoryGiB": 8,
                "Status": {
                    "State": "Enabled",
                    "Health": "OK",
                    "HealthRollUp": "OK"
                }
            },
            "Processors": {
                "@odata.id": "/redfish/v1/Systems/%s/Processors" % system_id},
            "EthernetInterfaces": {
                "@odata.id": "/redfish/v1/Systems/%s/EthernetInterfaces" % system_id
            },
            "SimpleStorage": {},
            "DimmConfig": {
                "@odata.id": "/redfish/v1/Systems/%s/DimmConfig" % system_id
            },
            "MemoryChunks": {
                "@odata.id": "/redfish/v1/Systems/%s/MemoryChunk" % system_id
            },
            "Links": {
                "Chassis": [{
                    "@odata.id": "/redfish/v1/Chassis/%s" % chassis_id
                }],
                "ManagedBy": [{
                    "@odata.id": "/redfish/v1/Managers/manager%d" % managedby
                }],
                "Oem": {}
            },
            "Actions": {
                "#ComputerSystem.Reset": {
                    "target":
                        "/redfish/v1/Systems/%s/Actions/ComputerSystem.Reset" % system_id,
                    "ResetType@Redfish.AllowableValues": [
                        "On",
                        "ForceOff",
                        "GracefulShutdown",
                        "ForceRestart",
                        "Nmi",
                        "GracefulRestart",
                        "ForceOn",
                        "PushPowerButton"]
                },
                "Oem": {
                    "Lenovo:RackScale": {
                        "#ComputerSystem.StartDeepDiscovery": {
                            "target":
                                "/redfish/v1/Systems/%s/Actions/ComputerSystem.StartDeepDiscovery" % system_id
                        },
                    }
                }
            },
            "Oem": {
                "Lenovo:RackScale": {
                    "Location": {
                        "Rack": "Rack" + str(chassis_location2[chassis_id][2]),
                        "ULocation": chassis_location2[chassis_id][0],
                        "UHeight": chassis_location2[chassis_id][1],
                        "Chassis": chassis_id
                    },
                    "@odata.type": "#Intel.Oem.ComputerSystem",
                    "Adapters": {
                        "@odata.id": "/redfish/v1/Systems/%s/Adapters" % system_id
                    },
                    "PciDevices": [{
                        "VendorId": "0x8086",
                        "DeviceId": "0x1234"
                    }],
                    "DiscoveryState": "Basic",
                    "ProcessorSockets": 8, "MemorySockets": 8
                }
            }
        }


# /redfish/v1/Systems/System1/Processors
class Processors(Resource):

    def get(self, system_id):
        members = get_members(
            "processor", "/redfish/v1/Systems/%s/Processors/" % system_id, 2)
        return {
            "@odata.context": "/redfish/v1/$metadata#Systems/Members/1/Processors/#entity",
            "@odata.id": "/redfish/v1/Systems/%s/Processors" % system_id,
            "@odata.type": "#ProcessorCollection.ProcessorCollection",
            "Name": "Processors Collection",
            "Members@odata.count": 2,
            "Members": members
        }


# /redfish/v1/Systems/System1/Processors/CPU1
class ProcessorDetail(Resource):

    def get(self, system_id, processor_id):
        system_id = str(system_id)
        number = int(filter(str.isdigit, system_id))
        if number <= 42:
            speed = '2700'
            model = "Multi-Core Intel(R) Xeon(R) processor E5 Series"
            totalcore = 4
        elif number <= 44:
            speed = '3200'
            model = "Multi-Core Intel(R) Xeon(R) processor E6 Series"
            totalcore = 8
        else:
            speed = '3400'
            model = "Multi-Core Intel(R) Xeon(R) processor E7 Series"
            totalcore = 8
        return {
            "@odata.context": "/redfish/v1/$metadata#Systems/Members/1/Processors/Members/$entity",
            "@odata.id": "/redfish/v1/Systems/%s/Processors/%s" % (system_id, processor_id),
            "@odata.type": "#Processor.1.0.0.Processor",
            "Name": processor_id,
            "Id": processor_id,
            "Socket": "",
            "ProcessorType": "CPU",
            "ProcessorArchitecture": "x86",
            "InstructionSet": "x86-64",
            "Manufacturer": "Intel(R) Corporation",
            "Model": model,
            "ProcessorId": {
                "VendorId": "GenuineIntel",
                "IdentificationRegisters": "0x34AC34DC8901274A",
                "EffectiveFamily": "0x42",
                "EffectiveModel": "0x61",
                "Step": "0x1",
                "MicrocodeInfo": "0x429943"
            },
            "MaxSpeedMHz": speed,
            "TotalCores": totalcore,
            "TotalThreads": totalcore * 2,
            "Status": {
                "State": "Enabled",
                "Health": "OK",
                "HealthRollup": "null"
            },
            "Oem": {
                "Intel:RackScale": {
                    "@odata.type": "#Intel.Oem.Processor",
                    "Brand": "E5",
                    "Capabilities": [
                        "sse",
                        "sse2",
                        "sse3"
                    ],
                    "ContainedBy": {
                        "@odata.id": "/redfish/v1/Systems/" + str(system_id)
                    }
                }
            }
        }


# /redfish/v1/Systems/{system_id}/DimmConfig
class DimmConfig(Resource):

    def get(self, system_id):
        system_id = str(system_id)
        number = int(filter(str.isdigit, system_id))
        if number <= 42:
            num = 4
        elif number <= 44:
            num = 6
        else:
            num = 8
        members = get_members(
            "dimm", "/redfish/v1/Systems/%s/DimmConfig/" % system_id, num)
        return {
            "@odata.context": "/redfish/v1/$metadata#Systems/Members/1/DimmConfig/$entity",
            "@odata.type": "#DimmConfigCollection.DimmConfigCollection",
            "@odata.id": "/redfish/v1/Systems/%s/DimmConfig" % system_id,
            "Name": "DIMM Configuration Collection",
            "Members@odata.count": num,
            "Members": members
        }


# /redfish/v1/Systems/System1/DIMMConfig/{memory_id}
class DIMMConfigDetail(Resource):

    def get(self, system_id, memory_id):
        system_id = str(system_id)
        memory_id = str(memory_id)
        number = int(filter(str.isdigit, system_id))
        uuid_ = str(uuid.uuid3(uuid.NAMESPACE_DNS, system_id + memory_id))
        manufacturer = 'Kingston USA'
        serialnumber = uuid_[-12:]
        partnumber = uuid_[9:18]
        if number <= 42:
            size = '8192'
            speed = '1333'
        elif number <= 44:
            size = '8192'
            speed = '1333'
        else:
            size = '16384'
            speed = '1600'
        return {
            "@odata.context": "/redfish/v1/$metadata#Systems/Members/1/DimmConfig/$entity",
            "@odata.id": "/redfish/v1/Systems/%s/DimmConfig/%s" % (system_id, memory_id),
            "@odata.type": "#DimmConfig.1.0.0.DimmConfig",
            "Name": memory_id,
            "Id": memory_id,
            "DimmType": "DRAM",
            "DimmDeviceType": "DDR" + str(number),
            "BaseModuleType": "LRDIMM",
            "DimmMedia": ["DRAM"],
            "CapacityMiB": size,
            "DataWidthBits": 64,
            "BusWidthBits": 72,
            "Manufacturer": manufacturer,
            "SerialNumber": serialnumber,
            "PartNumber": partnumber,
            "AllowedSpeedsMHz": [2133, 2400, 2667],
            "FirmwareRevision": "RevAbc",
            "FirmwareApiVersion": "ApiAbc",
            "FunctionClasses": ["Volatile"],
            "VendorId": "vendorX",
            "DeviceId": "deviceX",
            "RankCount": 1,
            "DeviceLocator": "PROC 1 DIMM 1",
            "DimmLocation": {
                "Socket": 1,
                "MemoryController": 1,
                "Channel": 1,
                "Slot": 1
            },
            "ErrorCorrection": "MultiBitECC",
            "Status": {
                "State": "Enabled",
                "Health": "OK",
                "HealthRollup": "null"
            },
            "OperatingSpeedMHz": speed,
            "Regions": [{
                "RegionId": "1",
                "MemoryType": "Volatile",
                "OffsetMiB": 0,
                "SizeMiB": 16384,
            }],
            "OperatingMemoryModes": [
                "1LM"
            ],
            "Oem": {
                "Intel:RackScale": {
                    "@odata.type": "#Intel.Oem.DimmConfig",
                    "VoltageVolt": 1.35
                }
            }
        }


# /redfish/v1/Systems/{system_id}/MemoryChunks
class MemoryChunks(Resource):

    def get(self, system_id):
        members = get_members(
            "chunk", "/redfish/v1/Systems/%s/MemoryChunk/" % system_id, 8)
        return {
            "@odata.context": "/redfish/v1/$metadata#Systems/Members/1/MemoryChunks/$entity",
            "@odata.id": "/redfish/v1/Systems/%s/MemoryChunk" % system_id,
            "@odata.type": "#MemoryChunkCollection.MemoryChunkCollection",
            "Name": "Memory Chunks Collection",
            "Members@odata.count": 8,
            "Members": members
        }


# /redfish/v1/Systems/System1/MemoryChunks/Chunk1
class MemoryChunkDetail(Resource):

    def get(self, system_id, chunk_id):
        number = chunk_id[-1:]
        return {
            "@odata.context": "/redfish/v1/$metadata#Systems/Members/1/MemoryChunks/$entity",
            "@odata.id": "/redfish/v1/Systems/%s/MemoryChunk/%s" % (system_id, chunk_id),
            "@odata.type": "#MemoryChunk.1.0.0.MemoryChunk",
            "Name": "Memory Chunk 1" + chunk_id,
            "Description": "description-as-string" + chunk_id,
            "Id": chunk_id,
            "MemoryChunkName": "name-as-string" + chunk_id,
            "MemoryChunkU_id": chunk_id,
            "MemoryChunkSizeMiB": 8192,
            "AddressRangeType": "Volatile",
            "IsMirrorEnabled": "false",
            "IsSpare": "false",
            "Status": {
                "State": "Enabled",
                "Health": "OK",
                "HealthRollup": "null"
            },
            "InterleaveSets": [{
                "@odata.id": "/redfish/v1/Systems/" + system_id + "/DimmConfig/dimm" + number,
                "RegionId": "1"
            }],
            "Oem": {}
        }


# /redfish/v1/Systems/{system_id}/Adapters
class Adapters(Resource):

    def get(self, system_id):
        members = get_members(
            "adapter", "/redfish/v1/Systems/%s/Adapters/" % system_id, 1)
        return {
            "@odata.context": "/redfish/v1/$metadata#Systems/Members/System1/Adapters",
            "@odata.id": "/redfish/v1/Systems/%s/Adapters" % system_id,
            "@odata.type": "#AdapterCollection.AdapterCollection",
            "Name": "Adapters Collection",
            "Members@odata.count": 1,
            "Members": members
        }


# /redfish/v1/Systems/{system_id}/Adapters/{adapter_id}
class AdapterDetail(Resource):

    def get(self, system_id, adapter_id):
        number = adapter_id[-1:]
        return {
            "@odata.context": "/redfish/v1/$metadata#Systems/Members/%s/Adapters/Members/$entity" % system_id,
            "@odata.id": "/redfish/v1/Systems/%s/Adapters/%s" % (system_id, adapter_id),
            "@odata.type": "#Adapter.1.0.0.Adapter",
            "Id": adapter_id,
            "Name": "StorageAdapter" + adapter_id,
            "Interface": "SATA",
            "Manufacturer": "Intel Corporation",
            "Model": "Wellsburg AHCI Controller",
            "Status": {
                "State": "Enabled",
                "Health": "OK",
                "HealthRollup": "OK"
            },
            "BusInfo": "pci@0000:01:00.0",
            "Oem": {},
            "Devices": {
                "@odata.id": "/redfish/v1/Systems/%s/Adapters/%s/Devices" % (system_id, adapter_id)
            },
            "Links": {
                "ContainedBy": {
                    "@odata.id": "/redfish/v1/Systems/%s" % system_id
                },
                "Oem": {}
            }
        }


# /redfish/v1/Systems/{system_id}/Adapters/{adapter_id}/Devices
class Devices(Resource):

    def get(self, system_id, adapter_id):
        system_id = str(system_id)
        number = int(filter(str.isdigit, system_id))
        if number <= 42:
            num = 1
        elif number <= 44:
            num = 2
        else:
            num = 4
        members = get_members(
            "device", "/redfish/v1/Systems/%s/Adapters/%s/Devices/" % (system_id, adapter_id), num)
        return {
            "@odata.context": "/redfish/v1/$metadata#Systems/Members/System1/Adapters/Members/Adapter1/Devices",
            "@odata.id": "/redfish/v1/Systems/%s/Adapters/%s/Devices" % (system_id, adapter_id),
            "@odata.type": "#DeviceCollection.DeviceCollection",
            "Name": "Devices Collection",
            "Members@odata.count": num,
            "Members": members
        }


# /redfish/v1/Systems/System1/Adapters/Adapter1/Devices/Device1
class DeviceDetail(Resource):

    def get(self, system_id, adapter_id, device_id):
        system_id = str(system_id)
        device_id = str(device_id)
        number = int(filter(str.isdigit, device_id))
        uuid_ = str(uuid.uuid3(uuid.NAMESPACE_DNS, system_id + device_id))
        manufacturer = 'Kingston USA'
        serialnumber = uuid_[-12:]
        if number <= 42:
            size = '300'
            model = 'ST500DM0-02'
        elif number <= 44:
            size = '500'
            model = 'MZ75E20B-CN'
        else:
            size = '1024'
            model = 'UT7725BI-23'
        return {
            "@odata.context": "/redfish/v1/Systems/Members/System1/Adapters/Members/Adapter1/Devices/Members/$entity",
            "@odata.id": "/redfish/v1/Systems/%s/Adapters/%s/Devices/%s" % (system_id, adapter_id, device_id),
            "@odata.type": "#Device.1.0.0.Device",
            "Id": device_id,
            "Name": device_id,
            "Interface": "SATA",
            "CapacityGiB": size,
            "Type": "HDD",
            "RPM": 0,
            "Manufacturer": manufacturer,
            "Model": model,
            "SerialNumber": serialnumber,
            "FirmwareVersion": "000",
            "BusInfo": "scsi@0:0.0.0",
            "Status": {
                "State": "Enabled",
                "Health": "OK",
                "HealthRollup": "null"
            },
            "Oem": {},
            "Links": {
                "ContainedBy": {
                    "@odata.id": "/redfish/v1/Systems/%s/Adapters/%s" % (system_id, adapter_id)
                },
                "Oem": {}
            }
        }


# GET /redfish/v1/Managers/{manager_id}/EthernetInterfaces
class ManagerEthernetInterfaces(Resource):

    def get(self, manager_id, ):
        members = get_members(
            "LAN", "/redfish/v1/Managers/%s/EthernetInterfaces/" % manager_id, 2)
        return {
            "@odata.context": "/redfish/v1/$metadata#Managers/Members/1/EthernetInterfaces/$entity",
            "@odata.id": "/redfish/v1/Managers/%s/EthernetInterfaces" % manager_id,
            "@odata.type": "#EthernetNetworkInterface.1.0.0.EthernetNetworkInterfaceCollection",
            "Name": "Ethernet Network Interface Collection",
            "Members@odata.count": 2,
            "Members": members
        }


# GET /redfish/v1/system/{system_id}/EthernetInterfaces
class SystemEthernetInterfaces(Resource):

    def get(self, system_id, ):
        members = get_members(
            "LAN", "/redfish/v1/Systems/%s/EthernetInterfaces/" % system_id, 2)
        return {
            "@odata.context": "/redfish/v1/$metadata#Managers/Members/1/EthernetInterfaces/$entity",
            "@odata.id": "/redfish/v1/Systems/%s/EthernetInterfaces" % system_id,
            "@odata.type": "#EthernetNetworkInterface.1.0.0.EthernetNetworkInterfaceCollection",
            "Name": "Ethernet Network Interface Collection",
            "Members@odata.count": 2,
            "Members": members
        }


# /redfish/v1/Systems/System1/EthernetInterfaces/{nic_id}  //+ VLANs + vlan_id
class SystemEthernetInterfacesDetail(Resource):

    def get(self, system_id, nic_id):
        system_id = str(system_id)
        nic_id = str(nic_id)
        mac_ = str(uuid.uuid3(uuid.NAMESPACE_DNS,
                              system_id + nic_id))[-12:].upper()
        mac = '%s:%s:%s:%s:%s:%s' % (mac_[0:2], mac_[2:4], mac_[4:6], mac_[
                                     6:8], mac_[8:10], mac_[10:])
        number = int(filter(str.isdigit, system_id))
        if '1' in nic_id:
            ip = '192.168.1.%d' % (100 + number)
        else:
            ip = '10.10.25.%d' % (100 + number)
        return {
            "@odata.context": "/redfish/v1/$metadata#EthernetInterface.EthernetInterface",
            "@odata.id": "/redfish/v1/Systems/%s/EthernetInterfaces/%s" % (system_id, nic_id),
            "@odata.type": "#EthernetInterface.1.0.0.EthernetInterface",
            "Id": nic_id,
            "Name": "Ethernet Interface " + nic_id,
            "Description": "System NIC",
            "Status": {
                "State": "Enabled",
                "Health": "OK",
                "HealthRollup": "null"
            },
            "InterfaceEnabled": "true",
            "PermanentMACAddress": mac,
            "MACAddress": mac,
            "SpeedMbps": 100,
            "AutoNeg": "true",
            "FullDuplex": "true",
            "MTUSize": 1500,
            "HostName": "web483",
            "FQDN": "web483.Redfishspecification.org",
            "IPv6DefaultGateway": "fe80::3ed9:2bff:fe34:600",
            "MaxIPv6StaticAddresses": "null",
            "NameServers": [
                "names.Redfishspecification.org"
            ],
            "IPv4Addresses": [
                {
                    "Address": ip,
                    "SubnetMask": "255.255.252.0",
                    "AddressOrigin": "Static",
                    "Gateway": "192.168.0.1"
                }
            ],
            "IPv6Addresses": [
                {
                    "Address": "fe80::1ec1:deff:fe6f:1e24",
                    "PrefixLength": 64,
                    "AddressOrigin": "Static",
                    "AddressState": "Preferred"
                }
            ],
            "IPv6StaticAddresses": [
            ],
            "VLAN": "null",
            "Oem": {},
            "Links": {
                "Oem": {
                    "Intel:RackScale": {
                        "@odata.type": "#Intel.Oem.EthernetInterface",
                        "NeighborPort": {
                            "@odata.id": "/redfish/v1/EthernetSwitches/switch1/Ports/port1"
                        }
                    }
                }
            }
        }


# /redfish/v1/manager/{manager_id}/EthernetInterfaces/{nic_id}    //+ VLANs + vlan_id
class ManagerEthernetInterfacesDetail(Resource):

    def get(self, manager_id, nic_id):
        return {
            "@odata.context": "/redfish/v1/$metadata#EthernetInterface.EthernetInterface",
            "@odata.id": "/redfish/v1/Managers/%s/EthernetInterfaces/%s" % (manager_id, nic_id),
            "@odata.type": "#EthernetInterface.1.0.0.EthernetInterface",
            "Id": nic_id,
            "Name": "Ethernet Interface " + nic_id,
            "Description": "System NIC",
            "Status": {
                "State": "Enabled",
                "Health": "OK",
                "HealthRollup": "null"
            },
            "InterfaceEnabled": "true",
            "PermanentMACAddress": "AA:BB:CC:DD:EE:FF",
            "MACAddress": "AA:BB:CC:DD:EE:FF",
            "SpeedMbps": 100,
            "AutoNeg": "true",
            "FullDuplex": "true",
            "MTUSize": 1500,
            "HostName": "web483",
            "FQDN": "web483.Redfishspecification.org",
            "IPv6DefaultGateway": "fe80::3ed9:2bff:fe34:600",
            "MaxIPv6StaticAddresses": "null",
            "NameServers": [
                "names.Redfishspecification.org"
            ],
            "IPv4Addresses": [
                {
                    "Address": "192.168.0.10",
                    "SubnetMask": "255.255.252.0",
                    "AddressOrigin": "Static",
                    "Gateway": "192.168.0.1"
                }
            ],
            "IPv6Addresses": [
                {
                    "Address": "fe80::1ec1:deff:fe6f:1e24",
                    "PrefixLength": 64,
                    "AddressOrigin": "Static",
                    "AddressState": "Preferred"
                }
            ],
            "IPv6StaticAddresses": [
            ],
            "VLAN": "null",
            "Oem": {},
            "Links": {
                "Oem": {
                    "Intel:RackScale": {
                        "@odata.type": "#Intel.Oem.EthernetInterface",
                        "NeighborPort": {
                            "@odata.id": "/redfish/v1/EthernetSwitches/switch1/Ports/port1"
                        }
                    }
                }
            }
        }


# /redfish/v1/Managers
class Managers(Resource):

    def get(self, ):
        members = get_members("manager", "/redfish/v1/Managers/", 11)
        return {
            "@odata.context": "/redfish/v1/$metadata#Managers",
            "@odata.id": "/redfish/v1/Managers",
            "@odata.type": "#Manager.1.0.0.ManagerCollection",
            "Name": "Manager Collection",
            "Members@odata.count": 11,
            "Members": members
        }


# /redfish/v1/Managers/manager_id
class ManagersDetail(Resource):

    def get(self, manager_id):
        manager_id = str(manager_id)
        number = int(filter(str.isdigit, manager_id))
        uuid_ = str(uuid.uuid3(uuid.NAMESPACE_DNS, manager_id))
        if number <= 2:
            type_ = 'RackManager'
            manager_location = 'Rack%d' % number
            if number == 1:
                manager_for_chassis = chassis_collection[
                    2:4] + chassis_collection[5:6] + chassis_collection[8:9]
                manager_for_servers = []
            else:
                manager_for_chassis = chassis_collection[
                    4:5] + chassis_collection[6:8] + chassis_collection[9:]
                manager_for_servers = []
        elif number <= 5:
            type_ = "EnclosureManager"
            manager_location = 'Chassis%d' % (number - 2)
            num = (number - 3) * 14
            manager_for_servers = get_members(
                "system", "/redfish/v1/Systems/", 48)[num:num + 14]
            manager_for_chassis = []
        else:
            type_ = "BMC"
            manager_location = 'Drawer%d' % (number - 5)
            num = number - 1
            manager_for_chassis = chassis_collection[num:num + 1]
            manager_for_servers = []
        return {
            "@odata.context": "/redfish/v1/$metadata#Manager.Manager",
            "@odata.id": "/redfish/v1/Managers/%s" % manager_id,
            "@odata.type": "#Manager.1.0.0.Manager",
            "Id": manager_id,
            "Name": "Manager" + manager_id,
            "ManagerType": type_,
            "Description": "Manager " + manager_id,
            "ServiceEntryPointUUID": uuid_[::-1],
            "UUID": uuid_,
            "Model": "Joo-Janta-200",
            "DateTime": "2015-03-13T04:14:33+06:0",
            "DateTimeLocalOffset": "+06:00",
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "GraphicalConsole": {
                "ServiceEnabled": "true",
                "MaxConcurrentSessions": 2,
                "ConnectTypesSupported": ["KVMIP"]
            },
            "SerialConsole": {
                "ServiceEnabled": "true",
                "MaxConcurrentSessions": 1,
                "ConnectTypesSupported": ["Telnet",
                                          "SSH",
                                          "IPMI"]
            },
            "CommandShell": {
                "ServiceEnabled": "true",
                "MaxConcurrentSessions": 4,
                "ConnectTypesSupported": ["Telnet",
                                          "SSH"]
            },
            "FirmwareVersion": "1.00",
            "NetworkProtocol": {
                "@odata.id": "/redfish/v1/Managers/%s/NetworkProtocol" % manager_id
            },
            "EthernetInterfaces": {
                "@odata.id": "/redfish/v1/Managers/%s/EthernetInterfaces" % manager_id
            },
            "Links": {
                "ManagerForServers": manager_for_servers,
                "ManagerForSwitches": [],
                "ManagerForChassis": manager_for_chassis,
                "ManagerLocation": {
                    "@odata.id": "/redfish/v1/Chassis/%s" % manager_location
                }, "Oem": {
                    "Intel:RackScale": {
                        "@odata.type": "#Intel.Oem.Manager",
                        "ManagerForServices": [{
                            "@odata.id": "/redfish/v1/Services/RSS1"
                        }]
                    }
                }
            },
            "Oem": {}
        }


# /redfish/v1/EthernetSwitches
class EthernetSwitches(Resource):

    def get(self, ):
        members = get_members("switch", "/redfish/v1/EthernetSwitches/", 2)
        return {
            "@odata.context": "/redfish/v1/$metadata#EthernetSwitches",
            "@odata.id": "/redfish/v1/EthernetSwitches",
            "@odata.type": "#EthernetSwitchesCollection.EthernetSwitchesCollection",
            "Name": "Ethernet Switches Collection",
            "Description": "Network Switches Collection",
            "Members@odata.count": 2,
            "Members": members
        }


# /redfish/v1/EthernetSwitches/Switch1
class EthernetSwitchesDetail(Resource):

    def get(self, switch_id):
        switch_id = str(switch_id)
        uuid_ = str(uuid.uuid3(uuid.NAMESPACE_DNS, switch_id))
        serialnumber = uuid_[-12:]
        partnumber = uuid_[9:18]
        return {
            "@odata.context": "/redfish/v1/$metadata#EthernetSwitch.EthernetSwitch",
            "@odata.id": "/redfish/v1/EthernetSwitches/" + switch_id,
            "@odata.type": "#EthernetSwitch.1.0.0.EthernetSwitch",
            "Id": switch_id,
            "SwitchId": switch_id,
            "Name": "PCIe-" + switch_id,
            "Description": "PCIe-" + switch_id,
            "Manufacturer": "Quanta",
            "Model": "ly8_rangley",
            "ManufacturingDate": "02/21/2015 00:00:00",
            "SerialNumber": serialnumber,
            "PartNumber": partnumber,
            "FirmwareName": "ONIE",
            "FirmwareVersion": "1.1",
            "Role": "TOR",
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "Oem": {},
            "Ports": {
                "@odata.id":
                    "/redfish/v1/EthernetSwitches/%s/Ports" % switch_id
            },
            "Links": {
                "Chassis": {
                    "@odata.id": "/redfish/v1/Chassis/chassis%s" % switch_id[-1:]
                },
                "ManagedBy": [{
                    "@odata.id": "/redfish/v1/Managers/manager1"
                }],
                "Oem": {}
            }
        }


# /redfish/v1/EthernetSwitches/Switch1/Ports
class Ports(Resource):

    def get(self, switch_id):
        members = get_members(
            "port", "/redfish/v1/EthernetSwitches/%s/Ports/" % switch_id, 8)
        return {
            "@odata.context": "/redfish/v1/$metadata#EthernetSwitches/Members/1/Ports",
            "@odata.id": "/redfish/v1/EthernetSwitches/%s/Ports" % switch_id,
            "@odata.type": "#SwitchPortsCollection.SwitchPortsCollection",
            "Name": "Ethernet Switch Port Collection" + switch_id,
            "Description": "Switch Port Collection" + switch_id,
            "Members@odata.count": 8,
            "Members": members
        }


# /redfish/v1/EthernetSwitches/Switch1/Ports/Port1
class PortDetail(Resource):

    def get(self, switch_id, port_id):
        number = port_id[-1:]
        return {
            "@odata.context": "/redfish/v1/$metadata#EthernetSwitches/Members/1/Ports/Members/1/$entity",
            "@odata.id": "/redfish/v1/EthernetSwitches/%s/Ports/%s" % (switch_id, port_id),
            "@odata.type": "#EthernetSwitchPort.1.0.0.EthernetSwitchPort",
            "Id": port_id,
            "Name": "Switch Port" + port_id,
            "PortId": "sw0p10" + port_id,
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "LinkType": "Ethernet",
            "OperationalState": "Up",
            "AdministrativeState": "Up",
            "LinkSpeedMbps": 10000,
            "NeighborInfo": {
                "SwitchId": "sw2",
                "PortId": "11",
                "CableId": "CustomerWritableThing"
            },
            "NeighborMAC": "00:11:22:33:44:55",
            "FrameSize": 1520,
            "Autosense": "true",
            "FullDuplex": "true",
            "MACAddress": "2c:60:0c:72:e6:33",
            "IPv4Addresses": [{
                "Address": "192.168.0.10",
                "SubnetMask": "255.255.252.0",
                "AddressOrigin": "Static",
                "Gateway": "192.168.0.1"
            }],
            "IPv6Addresses": [{
                "Address": "fe80::1ec1:deff:fe6f:1e24",
                "PrefixLength": 64,
                "AddressOrigin": "Static",
                "AddressState": "Preferred"
            }],
            "PortClass": "Logical",
            "PortMode": "LinkAggregationStatic",
            "PortType": "Upstream",
            "Oem": {},
            "VLANs": {"@odata.id":
                      "/redfish/v1/EthernetSwitches/" + switch_id + "/Ports/" + port_id + "/VLANs"
                      },
            "Links": {
                "PrimaryVLAN": {
                    "@odata.id":
                        "/redfish/v1/EthernetSwitches/" + switch_id +
                    "/Ports/" + port_id + "/VLANs/vlan" + number
                },
                "Switch": {
                    "@odata.id": "/redfish/v1/EthernetSwitches/" + switch_id
                },
                "MemberOfPort": {
                    "@odata.id": "/redfish/v1/EthernetSwitches/" + switch_id + "/Ports/" + port_id
                },
                "PortMembers": [],
                "Oem": {
                    "Intel:RackScale": {
                        "@odata.type": "#Intel.Oem.EthernetSwitchPort",
                        "NeighborInterface": {
                            "@odata.id": "/redfish/v1/Systems/system" + number + "/EthernetInterfaces/ethernetinterface" + number
                        }
                    }
                }
            }
        }


# /redfish/v1/EthernetSwitches/Switch1/Ports/Port1/VLANs
class SwitchVLANs(Resource):

    def get(self, switch_id, port_id):
        members = get_members(
            "vlan", "/redfish/v1/EthernetSwitches/%s/Ports/%s/VLANs/" % (switch_id, port_id), 8)
        return {
            "@odata.context": "/redfish/v1/$metadata#VLanNetworkInterfaceCollection.VLanNetworkInterfaceCollection",
            "@odata.id": "/redfish/v1/EthernetSwitches/" + switch_id + "/Ports/" + port_id + "/VLANs",
            "@odata.type": "#VLanNetworkInterfaceCollection.VLanNetworkInterfaceCollection",
            "Name": "VLAN Network Interface Collection",
            "Description": "VLAN Network Interface Collection",
            "Members@odata.count": 8,
            "Members": members
        }


# -------------------there are 3 urls to get [VLANs/vlan_id]------------------------------ #

# /redfish/v1/system/{system_id}/EthernetInterfaces/{nic_id}/VLANs
class SystemVlans(Resource):

    def get(self, system_id, nic_id):
        members = get_members("vlan", "/redfish/v1/Systems/" + system_id + "/EthernetInterfaces/" + nic_id + "/VLANs/",
                              8)
        return {
            "@odata.context": "/redfish/v1/$metadata#VLanNetworkInterfaceCollection.VLanNetworkInterfaceCollection",
            "@odata.id": "/redfish/v1/Systems/" + system_id + "/EthernetInterfaces/" + nic_id + "/VLANs",
            "@odata.type": "#VLanNetworkInterfaceCollection.VLanNetworkInterfaceCollection",
            "Name": "VLAN Network Interface Collection",
            "Description": "VLAN Network Interface Collection",
            "Members@odata.count": 8,
            "Members": members
        }


# /redfish/v1/manager/{manager_id}/EthernetInterfaces/{nic_id}/VLANs
class ManagerVlans(Resource):

    def get(self, manager_id, nic_id):
        members = get_members("vlan",
                              "/redfish/v1/Managers/" + manager_id +
                              "/EthernetInterfaces/" + nic_id + "/VLANs/",
                              8)
        return {
            "@odata.context": "/redfish/v1/$metadata#VLanNetworkInterfaceCollection.VLanNetworkInterfaceCollection",
            "@odata.id": "/redfish/v1/Managers/" + manager_id + "/EthernetInterfaces/" + nic_id + "/VLANs",
            "@odata.type": "#VLanNetworkInterfaceCollection.VLanNetworkInterfaceCollection",
            "Name": "VLAN Network Interface Collection",
            "Description": "VLAN Network Interface Collection",
            "Members@odata.count": 8,
            "Members": members
        }


# GET /redfish/v1/EthernetSwitches/Switch1/Ports/Port1/VLANs/{vlan_id}
class SwitchVlanDetail(Resource):

    def get(self, switch_id, port_id, vlan_id):
        return {
            "@odata.context": "/redfish/v1/$metadata#VLanNetworkInterface.VLanNetworkInterface",
            "@odata.id": "/redfish/v1/EthernetSwitches/" + switch_id + "/Ports/" + port_id + "/VLANs/" + vlan_id,
            "@odata.type": "#VLanNetworkInterface.1.0.0.VLanNetworkInterface",
            "Id": vlan_id,
            "Name": "VLAN Network Interface" + vlan_id,
            "Description": "System NIC 1 VLAN" + vlan_id,
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "VLANEnable": "true",
            "VLANId": vlan_id,
            "Oem": {
                "Intel:RackScale": {
                    "@odata.type": "#Intel.Oem.VLanNetworkInterface",
                    "Tagged": "false"
                }
            }
        }


# GET /redfish/v1/system/{system_id}/EthernetInterfaces/{nic_id}/VLANs/{vlan_id}
class SystemVlanDetail(Resource):

    def get(self, system_id, nic_id, vlan_id):
        return {
            "@odata.context": "/redfish/v1/$metadata#VLanNetworkInterface.VLanNetworkInterface",
            "@odata.id": "/redfish/v1/Systems/" + system_id + "/EthernetInterfaces/" + nic_id + "/VLANs/" + vlan_id,
            "@odata.type": "#VLanNetworkInterface.1.0.0.VLanNetworkInterface",
            "Id": vlan_id,
            "Name": "VLAN Network Interface" + vlan_id,
            "Description": "System NIC 1 VLAN" + vlan_id,
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "VLANEnable": "true",
            "VLANId": vlan_id,
            "Oem": {
                "Intel:RackScale": {
                    "@odata.type": "#Intel.Oem.VLanNetworkInterface",
                    "Tagged": "false"
                }
            }
        }


# GET /redfish/v1/manager/{manager_id}/EthernetInterfaces/{nic_id}/VLANs/{vlan_id}
class ManagerVlanDetail(Resource):

    def get(self, manager_id, nic_id, vlan_id):
        return {
            "@odata.context": "/redfish/v1/$metadata#VLanNetworkInterface.VLanNetworkInterface",
            "@odata.id": "/redfish/v1/Managers/" + manager_id + "/EthernetInterfaces/" + nic_id + "/VLANs/" + vlan_id,
            "@odata.type": "#VLanNetworkInterface.1.0.0.VLanNetworkInterface",
            "Id": vlan_id,
            "Name": "VLAN Network Interface" + vlan_id,
            "Description": "System NIC 1 VLAN" + vlan_id,
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "VLANEnable": "true",
            "VLANId": vlan_id,
            "Oem": {
                "Intel:RackScale": {
                    "@odata.type": "#Intel.Oem.VLanNetworkInterface",
                    "Tagged": "false"
                }
            }
        }


# GET /redfish/v1/Managers/{manager_id}/NetworkProtocol
class NetworkProtocol(Resource):

    def get(self, manager_id):
        return {
            "@odata.context": "/redfish/v1/$metadata#ManagerNetworkProtocol.ManagerNetworkProtocol",
            "@odata.id": "/redfish/v1/Managers/%S/NetworkProtocol" % manager_id,
            "@odata.type": "#ManagerNetworkProtocol.1.0.0.ManagerNetworkProtocol",
            "Id": "NetworkProtocol",
            "Name": "Manager Network Protocol",
            "Description": "Manager Network Service Status",
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "HostName": "mymanager",
            "FQDN": "mymanager.mydomain.com",
            "HTTP": {
                "ProtocolEnabled": "true",
                "Port": 80
            },
            "HTTPS": {
                "ProtocolEnabled": "true",
                "Port": 443
            },
            "IPMI": {
                "ProtocolEnabled": "true",
                "Port": 623
            },
            "SSH": {
                "ProtocolEnabled": "true",
                "Port": 22
            },
            "SNMP": {
                "ProtocolEnabled": "true",
                "Port": 161
            },
            "VirtualMedia": {
                "ProtocolEnabled": "true",
                "Port": 17988
            },
            "SSDP": {
                "ProtocolEnabled": "true",
                "Port": 1900,
                "NotifyMulticastIntervalSeconds": 600,
                "NotifyTTL": 5,
                "NotifyIPv6Scope": "Site"
            },
            "Telnet": {
                "ProtocolEnabled": "true",
                "Port": 23
            },
            "KVMIP": {"ProtocolEnabled": "true",
                      "Port": 5288
                      },
            "Oem": {}
        }


# /redfish/v1/EventService
class EventService(Resource):

    def get(self):
        return {
            "@odata.context": "/redfish/v1/$metadata#EventService",
            "@odata.id": "/redfish/v1/EventService",
            "@odata.type": "#EventService.1.0.0.EventService",
            "Id": "EventService",
            "Name": "Event Service",
            "Description": "Event Service",
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "ServiceEnabled": "true",
            "DeliveryRetryAttempts": 3,
            "DeliveryRetryIntervalSeconds": 60,
            "EventTypesForSubscription": [
                "StatusChange",
                "ResourceUpdated",
                "ResourceAdded",
                "ResourceRemoved",
                "Alert"
            ],
            "Subscriptions": {
                "@odata.id": "/redfish/v1/Subscriptions"
            },
            "Actions": {
                "#EventService.SendTestEvent": {
                    "target": "/redfish/v1/EventService/Actions/EventService.SendTestEvent",
                    "EventType@Redfish.AllowableValues": [
                        "StatusChange",
                        "ResourceUpdated",
                        "ResourceAdded",
                        "ResourceRemoved",
                        "Alert"
                    ]
                },
                "Oem": {}
            },
            "Oem": {}
        }


# /redfish/v1/EventService/Subscriptions        # Subscription = Assignment
class Subscriptions(Resource):

    def get(self, ):
        members = get_members("subscription", "/redfish/v1/Subscriptions/", 8)
        return {
            "@odata.context": "/redfish/v1/$metadata#EventService/Members/Events/$entity",
            "@odata.type": "#EventDestinationCollection.EventDestinationCollection",
            "Name": "Event Subscriptions Collection",
            "Members@odata.count": 8,
            "Members": members
        }


# GET /redfish/v1/EventService/Subscriptions/1
class SubscriptionDetail(Resource):

    def get(self, destination_id):
        return {
            "@odata.context": "/redfish/v1/$metadata#EventService/Members/Subscriptions/Members/$entity",
            "@odata.id": "/redfish/v1/Subscriptions/" + destination_id,
            "@odata.type": "#EventService.1.0.0.EventDestination",
            "Id": destination_id,
            "Name": "EventSubscription" + destination_id,
            "Description": "EventSubscription" + destination_id,
            "Destination": "http://192.168.1.1/" + destination_id,
            "EventTypes": ["ResourceAdded", "esourceRemoved"],
            "Context": "My Event",
            "Protocol": "Redfish"
        }


# /redfish/v1/Nodes
class Nodes(Resource):

    def get(self):
        members = get_members("node", "/redfish/v1/Nodes/", 6)
        return {
            "@odata.context": "/redfish/v1/$metadata#ComposedNodeCollection.ComposedNodeCollection",
            "@odata.id": "/redfish/v1/Nodes",
            "@odata.type": "#ComposedNodeCollection.CComposedNodeCollection",
            "Name": "Composed Node Collection",
            "Members@odata.count": 6,
            "Members": members
        }


# /redfish/v1/Nodes/{node_id}
class NodeDetail(Resource):

    def get(self, node_id):
        node_id = str(node_id)
        number = int(filter(str.isdigit, node_id))
        name = 'ServerNode%s' % str(number)
        description = 'Nova node%s' % str(number)
        uuid_ = str(uuid.uuid3(uuid.NAMESPACE_DNS, node_id))
        return {
            "@odata.context": "/redfish/v1/$metadata#Nodes/Members/$entity",
            "@odata.id": "/redfish/v1/Nodes/node" + str(number),
            "@odata.type": "#ComposedNode.1.0.0.ComposedNode",
            "Id": node_id,
            "Name": name,
            "Description": description,
            "SystemType": "Logical",
            "AssetTag": "free form asset tag",
            "Manufacturer": "Manufacturer Name - the same as Computer System",
            "Model": "Model Name - the same as Computer System",
            "SKU": "SKU - the same as Computer System",
            "SerialNumber": "2M220100SL - the same as Computer System",
            "PartNumber": "Computer1 - the same as Computer System",
            "UUID": uuid_,
            "HostName": "",
            "PowerState": "On",
            "BiosVersion": "P79 v1.00 (09/20/2013) - the same as Computer System",
            "Status": {
                "State": "Enabled",
                "Health": "OK",
                "HealthRollUp": "OK"
            },
            "Processors": {
                "Count": 2,
                "Model": "Multi-Core Intel(R) Xeon(R) processor 7xxx Series",
                "Status": {
                    "State": "Enabled",
                    "Health": "OK"
                }
            },
            "Memory": {
                "TotalSystemMemoryGiB": 32,
                "Status": {
                    "State": "Enabled",
                    "Health": "OK"
                }
            },
            "ComposedNodeState": "Allocated",
            "Boot": {
                "BootSourceOverrideEnabled": "Disabled",
                "BootSourceOverrideTarget": "None",
                "BootSourceOverrideTarget@Redfish.AllowableValues": [
                    "None",
                    "Pxe",
                    "Hdd"
                ]
            },
            "Oem": {},
            "Links": {
                "ComputerSystem": {
                    "@odata.id": "/redfish/v1/Systems/system" + str(number + 42)
                },
                "Processors": [
                    {
                        "@odata.id": "/redfish/v1/Systems/System1/Processors/CPU1"
                    }
                ],
                "Memory": [
                    {
                        "@odata.id": "/redfish/v1/Systems/System1/DimmConfig/Dimm1"
                    }
                ],
                "EthernetInterfaces": [
                    {
                        "@odata.id": "/redfish/v1/Systems/System1/EthernetInterfaces/LAN1"
                    }
                ],
                "LocalDrives": [
                    {
                        "@odata.id": "/redfish/v1/Services/service1/LogicalDrives/volume%d" % (number * 2 - 1)
                    },
                    {
                        "@odata.id": "/redfish/v1/Services/service1/LogicalDrives/volume%d" % (number * 2)
                    }
                ],
                "RemoteDrives": [
                    {
                        "@odata.id": "/redfish/v1/Services/RSS1/Targets/target1"
                    }
                ],
                "ManagedBy": [
                    {
                        "@odata.id": "/redfish/v1/Managers/PODM"
                    }
                ],
                "Oem": {}
            },
            "Actions": {
                "#ComposedNode.Reset": {
                    "target": "/redfish/v1/Systems/1/Actions/ComposedNode.Reset",
                    "ResetType@Redfish.AllowableValues": [
                        "On",
                        "ForceOff",
                        "GracefulRestart",
                        "ForceRestart",
                        "Nmi",
                        "ForceOn",
                        "PushPowerButton",
                        "GracefulShutdown"
                    ]
                },
                "#ComposedNode.Assemble": {
                    "target": "/redfish/v1/Systems/1/Actions/ComposedNode.Assemble"
                }
            }
        }


# /redfish/v1/Services
class Services(Resource):

    def get(self):
        members = get_members("service", "/redfish/v1/Services/", 1)
        return {
            "@odata.context": "/redfish/v1/$metadata#ServiceCollection.ServiceCollection",
            "@odata.id": "/redfish/v1/Services",
            "@odata.type": "#ServiceCollection.ServiceCollection",
            "Name": "Service Collection",
            "Members@odata.count": 1,
            "Members": members
        }


# /redfish/v1/Services/service_id
class ServiceDetail(Resource):

    def get(self, service_id):
        return {
            "@odata.context": "/redfish/v1/$metadata#Services/Members/1/$entity",
            "@odata.id": "/redfish/v1/Services/%s" % service_id,
            "@odata.type": "#StorageService.1.0.0.StorageService",
            "Id": service_id,
            "Name": service_id,
            "Description": "Storage Service",
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "RemoteTargets": {
                "@odata.id": "/redfish/v1/Services/%s/Targets" % service_id
            },
            "LogicalDrives": {
                "@odata.id": "/redfish/v1/Services/%s/LogicalDrives" % service_id
            },
            "Drives": {
                "@odata.id": "/redfish/v1/Services/RSS1/Drives"
            },
            "Oem": {},
            "Links": {
                "ManagedBy": [
                    {
                        "@odata.id": "/redfish/v1/Managers/RSS"
                    }
                ],
                "Oem": {}
            }
        }


# /redfish/v1/Services/service_id/LogicalDrives
class Logicals(Resource):

    def get(self, service_id):
        members = get_members(
            "volume", "/redfish/v1/Services/%s/LogicalDrives/" % service_id, 12)
        return {
            "@odata.context": "/redfish/v1/$metadata#LogicalDriveCollection.LogicalDriveCollection",
            "@odata.id": "/redfish/v1/Services/%s" % service_id,
            "@odata.type": "#LogicalDriveCollection.LogicalDriveCollection",
            "Name": "LogicalDrive Collection",
            "Members@odata.count": 12,
            "Members": members
        }


# /redfish/v1/Services/service_id/LogicalDrives/volume_id
class LogicalDetail(Resource):

    def get(self, service_id, volume_id):
        service_id = str(service_id)
        volume_id = str(volume_id)
        number = int(filter(str.isdigit, volume_id))
        if number <= 4:
            mode = 'LVG'
            size = '100'
            target = 1
        elif number <= 8:
            mode = 'PV'
            size = '200'
            target = 2
        else:
            mode = 'LV'
            size = '400'
            target = 3
        return {
            "@odata.context": "/redfish/v1/$metadata#LogicalDrives/Links/Members/$entity",
            "@odata.id": "/redfish/v1/Services/%s/LogicalDrives/%s" % (service_id, volume_id),
            "@odata.type": "#LogicalDrive.LogicalDrive",
            "Id": volume_id,
            "Name": volume_id,
            "Description": "Logical Drive " + str(number),
            "Status": {
                "State": "Enabled",
                "Health": "OK",
            },
            "Type": "LVM",
            "Mode": mode,
            "Protected": [1,2],
            "CapacityGiB": size,
            "Image": "Ubuntu 12.04.4LTS / Linux 3.11 / 2014.1",
            "Bootable": '',
            "Snapshot": '',
            "Oem": {},
            "Links": {
                "LogicalDrives": [
                ],
                "PhysicalDrives": [],
                "MasterDrive": {},
                "UsedBy": [],
                "Targets": [
                    {
                        "@odata.id": "/redfish/v1/Services/service1/Targets/target%d" % target
                    }
                ],
                "Oem": {}
            }
        }


# /redfish/v1/Services/service_id/Targets
class Targets(Resource):

    def get(self, service_id):
        members = get_members(
            "target", "/redfish/v1/Services/%s/Targets/" % service_id, 3)
        return {
            "@odata.context": "/redfish/v1/$metadata#LogicalDriveCollection.TargetCollection",
            "@odata.id": "/redfish/v1/Services/%s" % service_id,
            "@odata.type": "#LogicalDriveCollection.TargetCollection",
            "Name": "Target Collection",
            "Members@odata.count": 3,
            "Members": members
        }


# /redfish/v1/Services/service_id/Targets/target_id
class TargetDetail(Resource):

    def get(self, service_id, target_id):
        service_id = str(service_id)
        target_id = str(target_id)
        number = int(filter(str.isdigit, target_id))
        if number == 1:
            volume_list = volume_collection[0:4]
        elif number == 2:
            volume_list = volume_collection[4:8]
        else:
            volume_list = volume_collection[8:]
        return {
            "@odata.context": "/redfish/v1/$metadata#RemoteTargets/Links/Members/$entity",
            "@odata.id": "/redfish/v1/Services/1/Targets/%s" % target_id,
            "@odata.type": "#RemoteTarget.RemoteTarget",
            "Id": target_id,
            "Name": target_id,
            "Description": "RemoteTarget %s" % target_id,
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "Type": "NetworkStorage",
            "Address": [
                {
                    "iSCSI": {
                        "TargetLUN": volume_list,
                        "TargetIQN": "iqn.2015-01.com.example: ceph-ubuntu14",
                        "TargetPortalIP": "10.102.44.54",
                        "TargetPortalPort": 3260
                    }
                }
            ],
            "Initiator": [
                {
                    "iSCSI": {
                        "InitiatorIQN": "iqn.2015-01.com.example: fedora21"
                    }
                }
            ],
            "Oem": {},
            "Links": {}
        }


# -------------------------------------url---------------------------------- #

# all use string _id
def init_routes():
    api.add_resource(Redfishv1, "/redfish/v1")

    api.add_resource(Chassis, "/redfish/v1/Chassis")

    api.add_resource(ChassisDetail, "/redfish/v1/Chassis/<string:chassis_id>")

    api.add_resource(Systems, "/redfish/v1/Systems")

    api.add_resource(SystemDetail, "/redfish/v1/Systems/<string:system_id>")

    api.add_resource(
        Processors, "/redfish/v1/Systems/<string:system_id>/Processors")

    api.add_resource(ProcessorDetail,
                     "/redfish/v1/Systems/<string:system_id>/Processors/<string:processor_id>")

    api.add_resource(
        DimmConfig, "/redfish/v1/Systems/<string:system_id>/DimmConfig")

    api.add_resource(DIMMConfigDetail,
                     "/redfish/v1/Systems/<string:system_id>/DimmConfig/<string:memory_id>")

    api.add_resource(
        MemoryChunks, "/redfish/v1/Systems/<string:system_id>/MemoryChunk")

    api.add_resource(MemoryChunkDetail,
                     "/redfish/v1/Systems/<string:system_id>/MemoryChunk/<string:chunk_id>")

    api.add_resource(
        Adapters, "/redfish/v1/Systems/<string:system_id>/Adapters")

    api.add_resource(AdapterDetail,
                     "/redfish/v1/Systems/<string:system_id>/Adapters/<string:adapter_id>")

    api.add_resource(Devices,
                     "/redfish/v1/Systems/<string:system_id>/Adapters/<string:adapter_id>/Devices")

    api.add_resource(DeviceDetail,
                     "/redfish/v1/Systems/<string:system_id>/Adapters/<string:adapter_id>/Devices/<string:device_id>")

    api.add_resource(ManagerEthernetInterfaces,
                     "/redfish/v1/Managers/<string:manager_id>/EthernetInterfaces")

    api.add_resource(SystemEthernetInterfaces,
                     "/redfish/v1/Systems/<string:system_id>/EthernetInterfaces")

    api.add_resource(SystemEthernetInterfacesDetail,
                     "/redfish/v1/Systems/<string:system_id>/EthernetInterfaces/<string:nic_id>")

    api.add_resource(ManagerEthernetInterfacesDetail,
                     "/redfish/v1/Managers/<string:manager_id>/EthernetInterfaces/<string:nic_id>")

    api.add_resource(Managers, "/redfish/v1/Managers")

    api.add_resource(
        ManagersDetail, "/redfish/v1/Managers/<string:manager_id>")

    api.add_resource(EthernetSwitches, "/redfish/v1/EthernetSwitches")

    api.add_resource(EthernetSwitchesDetail,
                     "/redfish/v1/EthernetSwitches/<string:switch_id>")

    api.add_resource(
        Ports, "/redfish/v1/EthernetSwitches/<string:switch_id>/Ports")

    api.add_resource(PortDetail,
                     "/redfish/v1/EthernetSwitches/<string:switch_id>/Ports/<string:port_id>")

    api.add_resource(NetworkProtocol,
                     "/redfish/v1/Managers/<string:manager_id>/NetworkProtocol")

    api.add_resource(SwitchVLANs,
                     "/redfish/v1/EthernetSwitches/<string:switch_id>/Ports/<string:port_id>/VLANs")

    api.add_resource(SystemVlans,
                     "/redfish/v1/Systems/<string:system_id>/EthernetInterfaces/<string:nic_id>/VLANs")

    api.add_resource(ManagerVlans,
                     "/redfish/v1/Managers/<string:manager_id>/EthernetInterfaces/<string:nic_id>/VLANs")

    api.add_resource(SwitchVlanDetail,
                     "/redfish/v1/EthernetSwitches/<string:switch_id>/Ports/<string:port_id>/VLANs/<string:vlan_id>")

    api.add_resource(SystemVlanDetail,
                     "/redfish/v1/Systems/<string:system_id>/EthernetInterfaces/<string:nic_id>/VLANs/<string:vlan_id>")

    api.add_resource(ManagerVlanDetail,
                     "/redfish/v1/Managers/<string:manager_id>/EthernetInterfaces/<string:nic_id>/VLANs/<string:vlan_id>")

    api.add_resource(EventService, "/redfish/v1/EventService")

    api.add_resource(Subscriptions, "/redfish/v1/Subscriptions")

    api.add_resource(SubscriptionDetail,
                     "/redfish/v1/Subscriptions/<string:destination_id>")

    api.add_resource(Nodes, "/redfish/v1/Nodes")

    api.add_resource(NodeDetail, "/redfish/v1/Nodes/<string:node_id>")

    api.add_resource(Services, "/redfish/v1/Services")

    api.add_resource(ServiceDetail, "/redfish/v1/Services/<string:service_id>")

    api.add_resource(
        Logicals, "/redfish/v1/Services/<string:service_id>/LogicalDrives")

    api.add_resource(
        LogicalDetail, "/redfish/v1/Services/<string:service_id>/LogicalDrives/<string:volume_id>")

    api.add_resource(
        Targets, "/redfish/v1/Services/<string:service_id>/Targets")

    api.add_resource(
        TargetDetail, "/redfish/v1/Services/<string:service_id>/Targets/<string:target_id>")

    # for test
    api.add_resource(Test, "/test")

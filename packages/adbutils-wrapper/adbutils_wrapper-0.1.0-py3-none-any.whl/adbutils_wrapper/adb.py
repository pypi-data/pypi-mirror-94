# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : adb.py
# Time       ：2/9/21 15:04
# Author     ：Rodney Cheung
"""
from typing import List, Dict

import adbutils

from adbutils_wrapper.adbtool.am import ActivityManager
from adbutils_wrapper.adbtool.pm import PackageManager


class AdbTool:
    def __init__(self, package_manager=None, activity_manager=None):
        self.__package_manager: PackageManager = package_manager
        self.__activity_manager: ActivityManager = activity_manager

    @property
    def package_manager(self):
        return self.__package_manager

    @package_manager.setter
    def package_manager(self, value):
        self.__package_manager = value

    @property
    def activity_manager(self):
        return self.__activity_manager

    @activity_manager.setter
    def activity_manager(self, value):
        self.__activity_manager = value


class AdbUtilWrapper:

    def __init__(self, host: str, port: int):
        self.__adb_client = adbutils.AdbClient(host, port)
        self.__adb_tools_dict: Dict[str, AdbTool] = dict()

    def device_id_list(self) -> List[str]:
        res = list()
        for device in self.__adb_client.device_list():
            res.append(device.serial)
        return res

    def adb_tool(self, device_id: str):
        if device_id not in self.__adb_tools_dict.keys():
            adb_device = self.__adb_client.device(device_id)
            pm = PackageManager(adb_device)
            am = ActivityManager(adb_device)
            self.__adb_tools_dict[device_id] = AdbTool(pm, am)
        return self.__adb_tools_dict[device_id]

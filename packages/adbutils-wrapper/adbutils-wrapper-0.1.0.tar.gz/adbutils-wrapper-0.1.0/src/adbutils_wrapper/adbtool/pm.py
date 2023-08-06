# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : pm.py
# Time       ：2/10/21 08:41
# Author     ：Rodney Cheung
"""
from typing import Iterable, List

from adbutils import AdbDevice

from adbutils_wrapper.adbtool import BaseAdbTool


class PackageManager(BaseAdbTool):
    def __init__(self, device: AdbDevice):
        super().__init__(device)
        self.__cmd = 'pm'

    def install_app(self, apk_path: str, force: bool = False):
        """
        install app
        :param apk_path: apk path
        :param force: uninstall before install app
        :return:None
        """
        self.m_device.install(apk_path, force)

    def uninstall_app(self, pkg_name: str) -> bool:
        """
        uninstall app
        :param pkg_name: target app's package name
        :return: is success
        """
        return 'Success' in self.m_device.uninstall(pkg_name)

    def uninstall_app_for_user(self, user_id: str, pkg_name: str) -> bool:
        """
        uninstall app for specified user
        :param user_id: current user id,you can get it by
        ActivityManager.get_current_user_id()
        :param pkg_name:package name
        :return:is success
        """
        res = self.m_device.shell([self.__cmd, 'uninstall', '--user', user_id, pkg_name])
        return 'Success' in res

    def uninstall_apps_for_user(self, user_id: str, pkg_names: Iterable[str]) -> List[str]:
        """
        uninstall apps for specified user
        :param user_id: current user id,you can get it by
        ActivityManager.get_current_user_id()
        :param pkg_names: package name list
        :return: successfully uninstalled apps
        """
        suc_list = list()
        for pkg_name in pkg_names:
            if self.uninstall_app_for_user(user_id, pkg_name):
                suc_list.append(pkg_name)
        return suc_list

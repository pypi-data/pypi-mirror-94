# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : am.py
# Time       ：2/10/21 08:53
# Author     ：Rodney Cheung
"""
from adbutils import AdbDevice

from adbutils_wrapper.adbtool import BaseAdbTool


class ActivityManager(BaseAdbTool):
    def __init__(self, device: AdbDevice):
        super().__init__(device)
        self.__cmd: str = 'am'

    def get_current_user_id(self) -> str:
        """
        get current user id
        :return: user id
        """
        return self.m_device.shell([self.__cmd, 'get-current-user'])

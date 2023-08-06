# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : dumpsys.py
# Time       ：2/10/21 08:50
# Author     ：Rodney Cheung
"""
from adbutils import AdbDevice

from adbutils_wrapper.adbtool import BaseAdbTool


class Dumpsys(BaseAdbTool):
    def __init__(self, device: AdbDevice):
        super().__init__(device)

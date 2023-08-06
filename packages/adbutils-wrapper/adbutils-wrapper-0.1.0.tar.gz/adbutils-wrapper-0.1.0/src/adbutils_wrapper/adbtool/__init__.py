# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : __init__.py.py
# Time       ：2/10/21 09:05
# Author     ：Rodney Cheung
"""
from adbutils import AdbDevice


class BaseAdbTool:
    def __init__(self, device: AdbDevice):
        self.m_device: AdbDevice = device

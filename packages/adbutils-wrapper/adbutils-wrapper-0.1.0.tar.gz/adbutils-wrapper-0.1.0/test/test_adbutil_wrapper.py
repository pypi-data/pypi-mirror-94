# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_adbutil_wrapper.py
# Time       ：2/10/21 08:22
# Author     ：Rodney Cheung
"""
import os
import unittest

from adbutils_wrapper.adb import AdbUtilWrapper
from testdata import TestUtil


class TestAdbUtilsWrapper(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.adb_util_wrapper = AdbUtilWrapper('127.0.0.1', 5037)
        cls.device_id = cls.adb_util_wrapper.device_id_list()[0]
        cls.adb_tool = cls.adb_util_wrapper.adb_tool(cls.device_id)
        cls.pm = cls.adb_tool.package_manager
        cls.am = cls.adb_tool.activity_manager
        cls.pkg_name = 'com.cootek.smartinputv5.skin.keyboard_theme_colorful_thunder_neon_lights'

    def test_install_app(self):
        apk_path = os.path.join(TestUtil.get_test_data_path(), 'test.apk')
        self.pm.install_app(apk_path, True)

    def test_uninstall_app(self):
        self.assertEqual(self.pm.uninstall_app(self.pkg_name), True)

    def test_get_current_user_id(self):
        self.assertEqual(self.am.get_current_user_id(), '0')


if __name__ == '__main__':
    unittest.main()

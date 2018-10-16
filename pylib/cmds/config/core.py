# -*- coding: UTF-8 -*-
"""
flow config
certify a local workspace directory, or we can set 'd:\$username\workspace' as default value
"""
import os


class UserBO(object):
    def __init__(self):
        self.workspace = 'd:\{}\workspace'.format(os.uname())

    def set_workspace(self):
        pass

    def get_workspace(self):
        pass


class UserBiz(object):

    def change_workspace(self):
        pass
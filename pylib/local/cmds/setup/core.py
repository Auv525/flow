# -*- coding: UTF-8 -*-
"""
flow setup
"""
import os
import sys


class GetSetup(object):

    def get_user_settings(self):
        """get user settings"""
        pass

    def get_user_enter(self):
        """get user enter projects information"""
        pass


class DoClone(object):

    def clone_git_projects(self):
        """clone git projects"""
        pass

    def checkout_dev_branch(self):
        """checkout to dev branch"""
        pass


def run():
    """run function"""
    ScmClone.clone_git_projects()
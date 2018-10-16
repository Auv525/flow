# -*- coding: UTF-8 -*-
"""
flow cleanup
"""
import os
import sys


class CheckCleanup(object):

    def check_is_changed(self):
        pass

    def check_is_committed(self):
        pass

    def check_is_pushed(self):
        pass

    def check_remote_branch(self):
        pass


class GetCleanupAction(object):

    def possible_action(self):
        pass

    def get_people_action(self):
        pass


class DoCleanup(object):

    def cleanup_remote_branch(self):
        pass

    def cleanup_local_directory(self):
        pass
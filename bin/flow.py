# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
List all commands and arguments
"""
import os
import argparse
from local.cmds.push.core import run as push_run


class CommandBase(object):

    def push(self):
        paser = argparse.ArgumentParser(description='flow setup')
        # paser.add_argument()
        # args = paser.parse_args()
        push_run()


comm = CommandBase()
comm.push()
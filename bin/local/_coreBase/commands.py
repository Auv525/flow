# -*- coding: UTF-8 -*-
"""
List all commands and arguments
"""
import os
import argparse


class CommandBase(object):

    def setup(self):
        paser = argparse.ArgumentParser(description='setup')
        paser.add_argument()

        args = paser.parse_args()
# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
flow update core
"""
import argparse

from local.util.flow_projects import FlowProjectSpec
from local.util.git_workspace import *


class DoUpdate(object):
    """Do flow update"""

    pass


def prepare_update_parser(parser):
    """
    Create arguments for the "update" sub-command parser

    :param argparse.ArgumentParser parser: update parser
    :return: update parser with arguments
    """
    parser.add_argument('-v', "--verbose", action="store_true", default=False, dest="verbose")
    parser.set_defaults(func=run)
    return parser


def run():
    project_spec = FlowProjectSpec.prompt_user_to_specify(os.getcwd(), "update")
    project_workspace = project_spec.workspace
    print project_workspace.get_project_dirs_list()

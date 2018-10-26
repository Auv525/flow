# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
flow push
"""
import argparse

from local._coreBase.commandBasic import exec_commands, CheckStatus
from local.util.flowProjects import FlowProjectSpec
from local.util.workspace import *


class DoUpdate(object):
    pass


def prepare_update_parser(parser):
    """
    Create the parser argument for the "update" sub-command

    :param argparse.ArgumentParser parser:
    :return:
    """
    parser.add_argument('-v', "--verbose", action="store_true", default=False, dest="verbose")
    parser.set_defaults(func=run)
    return parser


def run():
    project_spec = FlowProjectSpec.prompt_user_to_initialize(os.getcwd())
    project_workspace = project_spec.workspace
    print project_workspace.get_project_dirs_list()

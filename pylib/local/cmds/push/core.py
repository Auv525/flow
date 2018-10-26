# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
flow push core
"""
import argparse

from local._coreBase.commandBasic import exec_commands
from local.util.git_project import GitProject
from local.util.flowProjects import FlowProjectSpec
from local.util.gitWorkspace import *


def prepare_push_parser(parser):
    """
    Create arguments for the "push" sub-command parser

    :param argparse.ArgumentParser parser: push parser
    :return: push parser with arguments
    """
    parser.add_argument('-v', "--verbose", action="store_true", default=False, dest="verbose")
    parser.set_defaults(func=run)
    return parser


def run(args):
    # find workspace of current dir and the active projects
    project_spec = FlowProjectSpec.prompt_user_to_specify(os.getcwd(), "push")
    project_dirs = project_spec.get_active_projects()

    # do flow push for these active projects
    for dir in project_dirs:
        if True:
            project = GitProject(dir)
            project.check_is_committed()
            current_branch = project.head_branch_name()
            if current_branch == "master":
                print "Please checkout into dev branch!"
                exit(1)
            project.rebase_master()
            project.push_branch()
            project.checkout_branch()
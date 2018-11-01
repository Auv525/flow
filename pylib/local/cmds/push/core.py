# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
flow push core
"""
import sys
import argparse

from local.util.git_project import GitProject
from local.util.flow_projects import FlowProjectSpec
from local.util.git_workspace import *


def prepare_push_parser(parser):
    """
    Create arguments for the "push" sub-command parser

    :param argparse.ArgumentParser parser: push parser
    :return: push parser with arguments
    """
    parser.add_argument('-v', '--verbose', action='store_true', default=False, dest='verbose')
    parser.set_defaults(func=run)
    return parser


def run(args):
    # find workspace of current dir and the active projects
    project_spec = FlowProjectSpec.prompt_user_to_specify(os.getcwd(), 'push')

    # do flow push for these active projects
    for dir in project_spec.get_active_projects():
        project = GitProject(dir)
        dev_branch = project.branch_name
        check_is_dev_branch(dir, dev_branch)
        check_is_dirty(project)
        project.rebase_master()

        project.checkout_branch('master')
        project.merge_branch(dev_branch)
        project.push_master()
        project.checkout_branch(dev_branch)


def check_is_dev_branch(dir, branch_name):
    """
    check if branch is dev branch and print info
    :param str dir: project directory
    :param str branch_name:
    :return:
    """

    if branch_name is None:
        print '\nYou are rebasing on {}'.format(dir)
        print 'Please fix conflicts!'
        sys.exit(1)

    if branch_name == 'master':
        print 'Please checkout into dev branch!'
        sys.exit(1)


def check_is_dirty(project):
    """check if branch is dirty and print info
    :param GitProject project: project object
    :return:
    """

    if project.is_dirty():
        print 'You have some changes to be committed!'
        sys.exit(1)


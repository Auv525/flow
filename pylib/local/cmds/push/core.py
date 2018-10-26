# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
flow push core
"""
import argparse

from local._coreBase.commandBasic import exec_commands, CheckStatus
from local.util.flowProjects import FlowProjectSpec
from local.util.workspace import *


class PrintStatus(CheckStatus):
    """Check status and print infos"""

    def check_is_changed(self):
        """check if branch is changed and print info"""

        if not self.is_changed():
            print "Nothing changed"
            exit(1)

        print "You have changed something!"  # TODO: for testing logic, remove this line later
        return True

    def check_is_committed(self):
        """check if branch is committed and print info"""

        if self.check_is_changed():
            if not self.is_committed():
                print "You have some changes to be committed!"
                exit(1)

            return True


class DoPush(object):
    """Do flow push"""

    def __init__(self, cwd, branch):
        self.flow_workspace = cwd
        self.flow_branch = branch
        self.flow_project = os.path.split(cwd)[1]

    def rebase_master(self):
        """rebase master branch"""
        msg, err = exec_commands(
            "git pull --rebase origin master", self.flow_workspace)
        print msg, err

    def push_branch(self):
        """merge dev branch into master and push master"""
        command = "git checkout master;git merge {};git push origin master".format(self.flow_branch)  # TODO:fix bug
        msg, err = exec_commands(command=command, cwd=self.flow_workspace)
        print msg, err

        if not err:
            print "{}/ {} has been pushed successfully!".format(self.flow_project, self.flow_branch)
        else:
            print "push error!"

    def checkout_branch(self):
        """checkout into dev branch"""
        exec_commands("git checkout {}".format(self.flow_branch), self.flow_workspace)


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
    project_workspace = project_spec.workspace
    project_dirs = project_spec.get_active_projects()
    print project_dirs

    # do flow push for these active projects
    for dir in project_dirs:
        flow_branch = project_workspace.get_branch_name(dir)
        print flow_branch
        # TODO: when branch is master, exit or prompt question
        print_status = PrintStatus(dir, flow_branch)
        if print_status.check_is_committed():
            do_push = DoPush(dir, flow_branch)
            do_push.rebase_master()
            do_push.push_branch()
            do_push.checkout_branch()

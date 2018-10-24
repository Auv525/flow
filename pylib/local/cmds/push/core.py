# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
flow push
"""
import argparse

from local._coreBase.commandBasic import exec_commands, CheckStatus
from local.util.flowProjects import FlowProjectSpec
from local.util.workspace import *


class PrintStatus(CheckStatus):
    """Check status and print infos"""
    # def check_is_changed(self):
    #     if self.is_changed():
    #         print "You have changed something!"
    #         return True

    def check_is_committed(self):
        if self.is_changed():
            if self.is_committed():
                return True
        else:
            if not self.is_committed():
                print "You have some changes to be committed!"
                exit(1)


class DoPush(object):
    def __init__(self, cwd, branch):
        self.flow_workspace = cwd
        self.flow_branch = branch
        self.flow_project = os.path.split(cwd)[1]

    def rebase_branch(self):
        """rebase master"""
        msg, err = exec_commands(
            "git pull --rebase origin master", self.flow_workspace)
        print msg, err

    def push_branch(self):
        """merge dev branch into master and push master"""
        command = "git checkout master;git merge {};git push origin master".format(self.flow_branch)  # TODO:
        msg, err = exec_commands(command=command, cwd=self.flow_workspace)
        # print "command: ", command
        # print msg, err
        if not err:
            print "{}/ {} has been pushed successfully!".format(self.flow_project, self.flow_branch)
        else:
            print "push error!"

    def checkout_branch(self):
        """checkout into branch"""
        exec_commands("git checkout {}".format(self.flow_branch), self.flow_workspace)


def push_prepare_parser(parser):
    """
    Create the parser argument for the "push" sub-command

    :param argparse.ArgumentParser parser:
    :return:
    """
    parser.add_argument('-v', "--verbose", action="store_true", default=False, dest="verbose")
    parser.set_defaults(func=run)
    return parser


def run(args):
    flow_workspace = Workspace([os.getcwd()])
    project_branch_dir = FlowProjectSpec(flow_workspace).prompt_user_to_initialize(os.getcwd())
    print project_branch_dir.workspace.projects_dir_branch
    # TODO: when branch is master, exit or prompt question
    for key, value in project_branch_dir.workspace.projects_dir_branch.items():
        print_status = PrintStatus(key, value)
        if print_status.check_is_committed():
            do_push = DoPush(key, value)
            do_push.rebase_branch()
            do_push.push_branch()
            do_push.checkout_branch()

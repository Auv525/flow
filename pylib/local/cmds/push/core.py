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
    project_spec = FlowProjectSpec.prompt_user_to_initialize(os.getcwd())
    project_workspace = project_spec.workspace
    print project_workspace.get_project_dirs_list()

    # TODO: when branch is master, exit or prompt question
    for dir in project_workspace.get_project_dirs_list():
        flow_branch = project_workspace.get_branch_name(dir)
        print_status = PrintStatus(dir, flow_branch)
        if print_status.check_is_committed():
            do_push = DoPush(dir, flow_branch)
            do_push.rebase_branch()
            do_push.push_branch()
            do_push.checkout_branch()

# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
flow push
"""
import os
import sys
import git
from local._coreBase.commandBasic import exec_commands, GitBase, CheckStatus


class FindProject(object):
    def __init__(self):
        self.current_path = r"D:\zhaochang\example_project\flow_test"  # TODO:later change into os.getcwd()
        self.project_name_list = []
        self.project_dir_set = set()
        self.projects_branches_dictionary = {}
        self.all_projects_enter = None

    def find_above_projects(self):
        """return above git projects directories set"""
        dir = self.current_path
        found = False
        while True:
            git_dir = os.path.join(dir, '.git')
            if git.repo.fun.is_git_dir(git_dir):
                found = True
                break

            dir = os.path.abspath(os.path.join(dir, '..'))
            if len(dir) < 5:  # TODO: Fix this, should be :is_root(dir)
                break

        if found:
            self.project_dir_set.add(dir)
            # find sister projects in workspace
            self.find_below_projects(os.path.split(dir)[0])
            self.all_projects_enter = raw_input(
                "You have these git projects: {}\nDo you want to push all of these projects or not? (y/n) ".format(
                    self.get_projects_names()))
            if not self.all_projects_enter.lower() in ['y', 'yes']:
                self.project_dir_set = set([dir])
            return self.project_dir_set

    def find_below_projects(self, dir):
        """
        return below git projects directories set
        :param dir:
        :return:
        """
        # dir = self.current_path
        for root, dirs, files in os.walk(dir):
            if git.repo.fun.is_git_dir(root):
                self.project_dir_set.add(os.path.split(root)[0])
        return self.project_dir_set

    def get_projects_names(self):
        """return projects names list"""
        for dir in self.project_dir_set:
            self.project_name_list.append(os.path.split(dir)[1])
        return self.project_name_list

    def get_projects_branches(self):
        """return projects branches dictionary"""
        for dir in self.project_dir_set:
            gitBase = GitBase(dir)
            head_branch = gitBase.get_head_branch()
            self.projects_branches_dictionary[dir] = head_branch.name

        return self.projects_branches_dictionary


class PrintStatus(CheckStatus):
    """Check status and print infos"""
    # def check_is_changed(self):
    #     if self.is_changed():
    #         print "You have changed something!"
    #         return True

    def check_is_committed(self):
        print self.is_changed()
        print self.is_committed()
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
        msg, err = exec_commands("git checkout master;git merge {};git push origin master".format(self.flow_branch), self.flow_workspace)
        print msg, err
        print "{}/ {} has been pushed successfully!".format(self.flow_project, self.flow_branch)

    def checkout_branch(self):
        """checkout into branch"""
        exec_commands("git checkout {}".format(self.flow_branch), self.flow_workspace)


def run():
    pro_ins = FindProject()
    if not pro_ins.find_above_projects():
        pro_ins.find_below_projects(r"D:\zhaochang\example_project\flow_test")
    project_branch_dir = pro_ins.get_projects_branches()
    for key, value in project_branch_dir.items():
        print_status = PrintStatus(key, value)
        if print_status.check_is_committed():
            do_push = DoPush(key, value)
            do_push.rebase_branch()
            do_push.push_branch()
            do_push.checkout_branch()

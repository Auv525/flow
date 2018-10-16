# -*- coding: UTF-8 -*-
"""
flow push
"""
import os
import sys
import git
from pylib._coreBase.commandBasic import GitBase, CheckStatus


class FindProject(object):
    def __init__(self):
        self.current_path = r"D:\zhaochang\example_project\bp"  # TODO:later change into os.getcwd()
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
        # dir = self.current_pathew
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

        print self.projects_branches_dictionary
        return self.projects_branches_dictionary


class PrintStatus(CheckStatus):
    """Check status and print infos"""
    def check_is_changed(self):
        if self.is_changed():
            print "You have changed something!"

    def check_is_committed(self):
        if not self.is_committed():
            print "You have some changes should be committed!"

    def check_is_pushed(self):
        if not self.is_pushed():
            print "You have some changes should be pushed!"


class DoPush(object):

    def rebase_branch(self):
        pass

    def checkout_branch(self, branch_name):
        pass

    def merge_branch(self):
        pass

    def push_branch(self):
        pass


if __name__ == '__main__':  # TODO:later change it into run()
    pro_ins = FindProject()
    if not pro_ins.find_above_projects():
        pro_ins.find_below_projects(r"D:\zhaochang\example_project\bp")
    project_branch_dir = pro_ins.get_projects_branches()
    for key, value in project_branch_dir.items():
        status = PrintStatus(value, key)
        status.check_is_changed()
        status.check_is_committed()
        status.check_is_pushed()
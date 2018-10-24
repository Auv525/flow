import os
from local._coreBase.commandBasic import GitBase


class Workspace(object):
    """workspace database"""
    def __init__(self, dirs):
        """
        :param dirs: list or set of dirs
        """
        self.projects_dir_name = {}
        for dir in dirs:
            project_name = os.path.split(dir)[1]
            self.projects_dir_name[project_name] = dir

        self.projects_dir_branch = {}
        for dir in dirs:
            print dir
            gitBase = GitBase(dir)
            head_branch = gitBase.get_head_branch()
            self.projects_dir_branch[dir] = head_branch.name

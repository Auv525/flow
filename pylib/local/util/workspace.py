import os
from collections import namedtuple
from local._coreBase.commandBasic import GitBase


FlowProjectInfo = namedtuple('FlowProjectInfo', ['dir', 'dir_name', 'git_name', 'branch'])


class Workspace(object):
    """workspace database"""

    def __init__(self, dirs):
        """
        :param dirs: list or set of dirs
        """
        self._project_infos = {}

        for dir in dirs:
            git_base = GitBase(dir)

            self._project_infos[dir] = FlowProjectInfo(
                dir=dir,
                dir_name=os.path.basename(dir),
                git_name=git_base.get_repository(),
                branch=git_base.get_head_branch().name
            )

    def get_project_dirs_list(self):
        return self._project_infos.keys()

    def get_project_name(self, dir):
        return self._project_infos[dir].git_name

    def get_branch_name(self, dir):
        return self._project_infos[dir].branch


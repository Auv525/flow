# !usr/bin/env python
# -*- coding: UTF-8 -*-
# Author    : ZhaoChang
# Email     : zhaochang525@126.com
import os
from collections import namedtuple

FlowProjectInfo = namedtuple('FlowProjectInfo', ['dir', 'dir_name'])


class GitWorkspace(object):
    """workspace database"""

    def __init__(self, dirs):
        """
        :param dirs: list or set of workspace dirs
        """
        self._project_infos = {}

        for dir in dirs:
            self._project_infos[dir] = FlowProjectInfo(
                dir=dir,
                dir_name=os.path.basename(dir)
            )

    def get_project_dirs_list(self):
        """Return project dirs list"""

        return self._project_infos.keys()

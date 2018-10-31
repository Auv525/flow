# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Basic functions in commands
"""
import subprocess


# TODO:remove this func later
def exec_commands(command, cwd):
    """
    run command in terminal
    :param command: command line
    :param cwd: command run in cwd
    :return:
    """

    return subprocess.check_output(command, cwd=cwd)

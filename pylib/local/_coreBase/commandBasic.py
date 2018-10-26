# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Basic functions in commands
"""
import subprocess


def exec_commands(command, cwd):
    """
    run command in terminal
    :param command: command line
    :param cwd: command run in cwd
    :return:
    """
    pr = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    msg = pr.stdout.read()
    err = pr.stderr.read()
    return msg, err

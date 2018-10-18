# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Basic functions in commands
"""
import os
import subprocess
import git


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


class GitBase(object):
    def __init__(self, git_workspace):
        self.git_workspace = git_workspace

    def check_git_repo(self):
        return git.repo.fun.is_git_dir(os.path.join(self.git_workspace, '.git'))

    def get_repository(self):
        """get git repository"""
        repo = git.Repo(self.git_workspace)
        return repo

    def get_head_branch(self):
        """get head branch name"""
        repo = self.get_repository()
        try:
            head_branch = repo.head.ref
            return head_branch
        except TypeError:
            print "You are rebasing on {}".format(self.git_workspace)
            print "Please fix conflicts!"

            exit(1)


class CheckStatus(object):
    """check project branch status"""
    def __init__(self, cwd, branch):
        self.flow_branch = branch
        self.cwd = cwd

    def is_changed(self):
        """if branch has been changed, return True"""
        local_sha, _ = exec_commands("git rev-parse \"{}\"".format(self.flow_branch), self.cwd)
        master_sha, err = exec_commands("git ls-remote origin | find \"master\"", self.cwd)
        if local_sha:
            if local_sha.split()[0] not in master_sha:
                return True

    def is_committed(self):
        """if nothing to be committed, return True"""
        git_repo = git.Repo(self.cwd)
        if "nothing to commit" in git_repo.git.status():
            return True
        else:
            return False

    def is_pushed(self):
        """if branch has been pushed, return True"""
        local_id, _ = exec_commands("git rev-parse HEAD", self.cwd)
        remote_id, _ = exec_commands("git ls-remote origin | find \"{}\"".format(self.flow_branch), self.cwd)
        try:
            if remote_id.split()[0] in local_id:
                return True
            else:
                return False
        except IndexError:
            return False

    def is_merged(self):
        """if branch has been merged into master, return True"""
        remote_id, _ = exec_commands("git ls-remote origin | find \"{}\"".format(self.flow_branch), self.cwd)
        master_id, _ = exec_commands("git ls-remote origin | find \"master\"", self.cwd)
        try:
            if remote_id.split()[0] in master_id:
                return True
            else:
                return False
        except IndexError:
            return False
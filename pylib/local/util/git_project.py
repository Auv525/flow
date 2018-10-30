import sys
import git
import subprocess
from local._core_base.command_basic import exec_commands


class GitProject(object):
    """
    Operate on git projects.
    Can check branch status, push and update branches.
    """

    def __init__(self, directory):
        self.project_directory = directory
        self._repository = git.Repo(self.project_directory)
        try:
            self._head_branch = self._repository.head.ref
            self.branch_name = self._head_branch.name
        except TypeError:
            self._head_branch = None
            self.branch_name = None

        # the sha key for current HEAD on the current branch
        self.local_binsha = self._repository.head.commit.binsha or None
        self.local_hexsha = self._repository.head.commit.hexsha or None
        # the remote master sha keys
        self.master_sha = exec_commands("git ls-remote origin | find \"master\"", self.project_directory) or None

    def check_is_dev_branch(self):
        """check if HEAD branch is dev branch"""

        if self.branch_name is None:
            print '\nYou are rebasing on {}'.format(self.project_directory)
            print 'Please fix conflicts!'
            sys.exit(1)

        if self.branch_name == 'master':
            print 'Please checkout into dev branch!'
            sys.exit(1)

    def is_committed(self):
        """if nothing to be committed, return True"""

        return self._repository.is_dirty()

    def is_pushed(self):
        """if branch has been pushed, return True"""

        remote_id = exec_commands("git ls-remote origin | find \'{}\'".format(self.branch_name), self.project_directory)
        try:
            return remote_id.split()[0] in self.local_hexsha
        except IndexError:
            return False

    def is_merged(self):
        """if branch has been merged into master, return True"""

        remote_id = exec_commands("git ls-remote origin | find \'{}\'".format(self.branch_name), self.project_directory)
        master_id = exec_commands("git ls-remote origin | find \'master\'", self.project_directory)
        try:
            return remote_id.split()[0] in master_id
        except IndexError:
            return False

    def check_is_committed(self):
        """check if branch is committed and print info"""

        if not self.is_committed():
            print 'You have some changes to be committed!'
            sys.exit(1)

    def rebase_master(self):
        """rebase master branch"""

        try:
            exec_commands('git pull --rebase origin master', self.project_directory)
        except subprocess.CalledProcessError:
            raise RebaseConflictEncountered

    def merge_to_master_and_push_master(self):
        """merge dev branch into master and push master"""

        exec_commands('git checkout master', self.project_directory)
        exec_commands('git merge {}'.format(self.branch_name), self.project_directory)
        exec_commands('git push origin master', self.project_directory)

    def checkout_branch(self, branch):
        """checkout into specify branch"""

        exec_commands('git checkout {}'.format(branch), self.project_directory)

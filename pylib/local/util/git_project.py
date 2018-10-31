import sys
import git
import subprocess


class GitProject(object):
    """
    Operate on git projects.
    Can check branch status, push and update branches.
    """

    def __init__(self, directory):
        self.project_directory = directory
        self._repository = git.Repo(self.project_directory)
        self.master_branch = self._repository.heads.master
        try:
            # self.active_branch = self._repository.head.ref
            self.head_branch = self._repository.head.ref   # TODO:test when rebasing, it raise TypeError
            self.branch_name = self.head_branch.ref.name
        except TypeError:
            self.branch_name = None

        # the sha key for current HEAD on the current branch
        self.local_binsha = self._repository.head.commit.binsha or None
        self.local_hexsha = self._repository.head.commit.hexsha or None

    def check_is_dev_branch(self):
        """check if HEAD branch is dev branch"""

        if self.branch_name is None:
            print '\nYou are rebasing on {}'.format(self.project_directory)
            print 'Please fix conflicts!'
            sys.exit(1)

        if self.branch_name == 'master':
            print 'Please checkout into dev branch!'
            sys.exit(1)

    def _is_committed(self):
        """if nothing to be committed, return True"""

        return self._repository.is_dirty()

    def _is_pushed(self):
        """if branch has been pushed, return True"""

        remote_id = subprocess.check_output("git ls-remote origin | find \'{}\'".format(self.branch_name), cwd=self.project_directory)
        try:
            return remote_id.split()[0] in self.local_hexsha
        except IndexError:
            return False

    def _is_merged(self):
        """if branch has been merged into master, return True"""

        remote_id = subprocess.check_output("git ls-remote origin | find \'{}\'".format(self.branch_name), cwd=self.project_directory)
        master_id = subprocess.check_output("git ls-remote origin | find \'master\'", cwd=self.project_directory)
        try:
            return remote_id.split()[0] in master_id
        except IndexError:
            return False

    def check_is_committed(self):
        """check if branch is committed and print info"""

        if not self._is_committed():
            print 'You have some changes to be committed!'
            sys.exit(1)

    def rebase_master(self):
        """rebase master branch"""

        try:
            subprocess.check_output('git pull --rebase origin master', cwd=self.project_directory)
        except subprocess.CalledProcessError:
            sys.exit(1)

    def checkout_branch(self, branch):
        """
        checkout branch
        :param HEAD branch: HEAD object should be checkout into
        :return:
        """

        # subprocess.check_output('git checkout {}'.format(branch), cwd=self.project_directory)
        branch.checkout()    # TODO:use HEAD or name?

    def merge_branch(self, branch):
        # TODO:change with gitPython
        subprocess.check_output('git merge {}'.format(branch), cwd=self.project_directory)
        # self._repository.merge_base(branch, self.master_branch)

    def push_master(self):
        # TODO:change with gitPython
        subprocess.check_output('git push origin master', cwd=self.project_directory)

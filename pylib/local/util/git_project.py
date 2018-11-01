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
        try:
            self.branch_name = self._repository.head.ref.name
        except TypeError:
            self.branch_name = None

        # the sha key for current HEAD on the current branch
        self.local_sha = self._repository.head.commit.hexsha or None

    def is_dirty(self):
        """if nothing to be committed, return True"""

        return self._repository.is_dirty()

    def is_pushed(self):
        """if branch has been pushed, return True"""

        remote_id = subprocess.check_output("git ls-remote origin | find \'{}\'".format(self.branch_name),
                                            cwd=self.project_directory)
        try:
            return remote_id.split()[0] in self.local_sha
        except IndexError:
            return False

    def is_merged(self):
        """if branch has been merged into master, return True"""

        remote_id = subprocess.check_output("git ls-remote origin | find \'{}\'".format(self.branch_name),
                                            cwd=self.project_directory)
        master_id = subprocess.check_output("git ls-remote origin | find \'master\'", cwd=self.project_directory)
        try:
            return remote_id.split()[0] in master_id
        except IndexError:
            return False

    def rebase_master(self):
        """rebase master branch"""
        subprocess.check_output('git pull --rebase origin master', cwd=self.project_directory)

    def checkout_branch(self, branch):
        """
        checkout into a specify branch
        :param str branch: name of branch which should be checkout into
        :return:
        """

        subprocess.check_output('git checkout {}'.format(branch), cwd=self.project_directory)

    def merge_branch(self, branch):
        """merge a specify branch"""

        subprocess.check_output('git merge {}'.format(branch), cwd=self.project_directory)

    def push_master(self):
        """push master branch"""

        subprocess.check_output('git push origin master', cwd=self.project_directory)

    def retrieve_change(self):
        """stash changes, rebase master and stash out"""
        subprocess.check_output('git stash', cwd=self.project_directory)
        self.rebase_master()
        subprocess.check_output('git stash pop', cwd=self.project_directory)

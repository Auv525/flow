import sys
import git
from local._core_base.command_basic import exec_commands


class GitProject(object):
    """
    Operate on git projects.
    Can check branch status, push and update branches.
    """

    def __init__(self, directory):
        self.project_directory = directory
        self.dev_branch = None
        self.repository = git.Repo(self.project_directory)

    def get_head_branch(self):
        """get head branch name"""

        try:
            head_branch = self.repository.head.ref
            if head_branch.name == "master":
                print "Please checkout into dev branch!"
                sys.exit(1)
            self.dev_branch = head_branch.name
            return self.dev_branch
        except TypeError:
            print "\nYou are rebasing on {}".format(self.project_directory)
            print "Please fix conflicts!"
            sys.exit(1)

    # not use this func now, use it later if necessary
    def is_changed(self):
        """if branch has been changed, return True"""

        # get the sha key for current HEAD on the current branch
        local_sha = exec_commands("git rev-parse \"{}\"".format(self.dev_branch), self.project_directory)
        # get the remote master sha keys
        master_sha = exec_commands("git ls-remote origin | find \"master\"", self.project_directory)
        if local_sha:
            return local_sha.split()[0] not in master_sha
        else:
            return None

    def is_committed(self):
        """if nothing to be committed, return True"""

        return "nothing to commit" in self.repository.git.status()

    def is_pushed(self):
        """if branch has been pushed, return True"""

        local_id = exec_commands("git rev-parse HEAD", self.project_directory)
        remote_id = exec_commands("git ls-remote origin | find \"{}\"".format(self.dev_branch), self.project_directory)
        try:
            return remote_id.split()[0] in local_id
        except IndexError:
            return False

    def is_merged(self):
        """if branch has been merged into master, return True"""

        remote_id = exec_commands("git ls-remote origin | find \"{}\"".format(self.dev_branch), self.project_directory)
        master_id = exec_commands("git ls-remote origin | find \"master\"", self.project_directory)
        try:
            return remote_id.split()[0] in master_id
        except IndexError:
            return False

    # not use this func now, use it later if necessary
    def check_is_changed(self):
        """check if branch is changed and print info"""

        if not self.is_changed():
            print "Nothing changed"
            sys.exit(0)

        print "You have changed something!"  # TODO: for testing logic, remove this line later

    def check_is_committed(self):
        """check if branch is committed and print info"""

        if not self.is_committed():
            print "You have some changes to be committed!"
            sys.exit(1)

    def rebase_master(self):
        """rebase master branch"""

        return exec_commands("git pull --rebase origin master", self.project_directory)

    def push_branch(self):
        """merge dev branch into master and push master"""

        command = ["git checkout master", "git merge {}".format(self.dev_branch), "git push origin master"]  # TODO:fix bug
        return exec_commands(command, self.project_directory)

    def checkout_branch(self):
        """checkout into dev branch"""

        return exec_commands("git checkout {}".format(self.dev_branch), self.project_directory)

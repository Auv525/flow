import os
import git
from local._coreBase.commandBasic import exec_commands


class GitProject(object):
    def __init__(self, directory):
        self.project_directory = directory
        self.dev_branch = None
        self.repository = git.Repo(self.project_directory)

    # def is_git_repo(self):
    #     return git.repo.fun.is_git_dir(os.path.join(self.project_directory, '.git'))

    def head_branch_name(self):
        """get head branch name"""
        my_repo = git.Repo(self.project_directory)
        try:
            head_branch = my_repo.head.ref
            self.dev_branch = head_branch.name
            return self.dev_branch
        except TypeError:
            print "\nYou are rebasing on {}".format(self.project_directory)
            print "Please fix conflicts!"
            exit(1)

    def is_changed(self):
        """if branch has been changed, return True"""
        local_sha, _ = exec_commands("git rev-parse \"{}\"".format(self.dev_branch), self.project_directory)
        master_sha, err = exec_commands("git ls-remote origin | find \"master\"", self.project_directory)
        if local_sha:
            if local_sha.split()[0] not in master_sha:
                return True
            else:
                return False

    def is_committed(self):
        """if nothing to be committed, return True"""
        git_repo = git.Repo(self.project_directory)
        if "nothing to commit" in git_repo.git.status():
            return True
        else:
            return False

    def is_pushed(self):
        """if branch has been pushed, return True"""
        local_id, _ = exec_commands("git rev-parse HEAD", self.project_directory)
        remote_id, _ = exec_commands("git ls-remote origin | find \"{}\"".format(self.dev_branch), self.project_directory)
        try:
            if remote_id.split()[0] in local_id:
                return True
            else:
                return False
        except IndexError:
            return False

    def is_merged(self):
        """if branch has been merged into master, return True"""
        remote_id, _ = exec_commands("git ls-remote origin | find \"{}\"".format(self.dev_branch), self.project_directory)
        master_id, _ = exec_commands("git ls-remote origin | find \"master\"", self.project_directory)
        try:
            if remote_id.split()[0] in master_id:
                return True
            else:
                return False
        except IndexError:
            return False

    def check_is_changed(self):
        """check if branch is changed and print info"""

        if not self.is_changed():
            print "Nothing changed"
            exit(1)

        print "You have changed something!"  # TODO: for testing logic, remove this line later
        return True

    def check_is_committed(self):
        """check if branch is committed and print info"""

        if self.check_is_changed():
            if not self.is_committed():
                print "You have some changes to be committed!"
                exit(1)

            return True

    def rebase_master(self):
        """rebase master branch"""
        msg, err = exec_commands(
            "git pull --rebase origin master", self.project_directory)
        print msg, err

    def push_branch(self):
        """merge dev branch into master and push master"""
        command = "git checkout master;git merge {};git push origin master".format(self.dev_branch)  # TODO:fix bug
        msg, err = exec_commands(command=command, cwd=self.project_directory)
        print msg, err

        if not err:
            print "{}/ {} has been pushed successfully!".format(os.path.basename(self.project_directory), self.dev_branch)
        else:
            print "push error!"

    def checkout_branch(self):
        """checkout into dev branch"""
        exec_commands("git checkout {}".format(self.dev_branch), self.project_directory)

import sys


def check_is_dev_branch(dir, branch_name):
    """
    check if branch is dev branch and print info
    :param str dir: project directory
    :param str branch_name:
    :return:
    """

    if branch_name is None:
        print '\nYou are rebasing in {}'.format(dir)
        print 'Please fix conflicts!'
        sys.exit(1)

    if branch_name == 'master':
        print 'Please checkout into dev branch!'
        sys.exit(1)


def check_is_dirty(project):
    """check if branch is dirty and print info
    :param GitProject project: project object
    :return:
    """

    if project.is_dirty():
        print 'You have some changes to be committed!'
        sys.exit(1)
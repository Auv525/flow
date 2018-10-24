import os
import git


def find_enclosing_git_project(dir):
    """
    Returns the path to the directory at the current level or above
    If there is no such directory, it returns None

    :param str dir:
    :return:
    """

    found = False
    while True:
        git_dir = os.path.join(dir, '.git')
        if git.repo.fun.is_git_dir(git_dir):
            found = True
            break

        dir = os.path.abspath(os.path.join(dir, '..'))
        if len(dir) < 5:  # TODO: Fix this, should be :is_root(dir)
            break

    if found:
        return dir
    else:
        return None


def find_child_projects(dir):
    """
    Returns a set of subdirectories (only one level deep) that are git projects

    :param str dir:
    :return:
    """

    project_dir_set = set()
    for root, dirs, files in os.walk(dir):  # TODO: change into one level deep only
        if git.repo.fun.is_git_dir(root):
            project_dir_set.add(os.path.split(root)[0])
    return project_dir_set


def get_projects_names(project_dir_set):
    """
    Returns project names list

    :param set project_dir_set:
    :return:
    """
    project_name_list = []
    for dir in project_dir_set:
        project_name_list.append(os.path.split(dir)[1])
    return project_name_list
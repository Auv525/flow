import os
import sys

from local.util.gitProjects import find_enclosing_git_project, find_child_projects, get_projects_names
from local.util.workspace import Workspace


class FlowProjectSpec(object):

    def __init__(self, workspace, active_project=None):
        """
        Keeps track of which part of a Workspace Flow should operate on.

        If active_project is None, then that means all projects.
        If active_project is a string, then only that project.

        :param Workspace workspace:
        :param active_project:
        :return:
        """

        self.workspace = workspace
        self.active = active_project
        print "workspace: ", self.workspace
        print "active: ", self.active
        # assert self.active in self.workspace.projects_dir_name

    @classmethod
    def prompt_user_to_initialize(cls, dir, action=None):
        """
        This method will, if needed, ask the user for clarification about the intended action

        :param str dir:
        :param str action: a string that will be used when interaction with the user
        :return:
        """
        pp = find_enclosing_git_project(dir)
        print "enclosing: ", pp
        if pp is not None:
            cp = find_child_projects(os.path.split(dir)[0])
            print "child: ", cp
            if cp:
                """
                if user says all, then do: return FlowProjectSpec(workspace)
                if user says only one, then do: return FlowProjectSpec(workspace, cwd)
                """
                all_projects_enter = raw_input(
                    "You have these git projects: {}\nDo you want to push all of these projects or not? (y/n) ".format(
                        get_projects_names(cp)))
                if all_projects_enter.lower() in ['y', 'yes']:
                    workspace = Workspace(cp)
                    return FlowProjectSpec(workspace)
                else:
                    workspace = Workspace([dir])
                    return FlowProjectSpec(workspace, dir)

        else:
            cp = find_child_projects(dir)
            if len(cp):
                print 'bad workspace'
                sys.exit(1)
            workspace = Workspace([dir])
            return FlowProjectSpec(workspace)

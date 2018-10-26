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

        :param Workspace workspace: Workspace object
        :param str active_project: active project name
        :return:
        """

        self.workspace = workspace
        self.active = active_project
        print "workspace: ", self.workspace
        print "active: ", self.active
        # assert self.active in self.workspace.projects_dir_name

    def get_active_projects(self):
        """
        Returns a list of projects directories that should be acted upon.

        :return: a list of projects directories
        :rtype: list
        """

        if self.active:
            return [self.active]
        else:
            return self.workspace.get_project_dirs_list()

    @classmethod
    def prompt_user_to_initialize(cls, dir, action=None):
        """
        This method will, if needed, ask the user for clarification about the intended action

        :param str dir: the directory where the search for workspace should begin
        :param str action: an action that will operate
        :return:
        """
        enclosing_project = find_enclosing_git_project(dir)
        print "enclosing: ", enclosing_project
        if enclosing_project is not None:
            # if we found a git project, we assume its parent is a workspace dir
            workspace_dir = os.path.dirname(enclosing_project)

            # let's test that theory
            child_projects = find_child_projects(workspace_dir)
            print "child: ", child_projects
            # if child_projects is None:
            #     raise RuntimeError("Bad")

            workspace = Workspace(child_projects)
            prompt = 'You have these git projects: {p}\nDo you want to {a} all of these projects or not? (y/n) '.format(
                    p=get_projects_names(child_projects),
                    a=action
                )
            all_projects_enter = raw_input(prompt)

            """
            if user says all, then do: return FlowProjectSpec(workspace)
            if user says only one, then do: return FlowProjectSpec(workspace, cwd)
            """
            if all_projects_enter.lower() in ['y', 'yes']:
                return FlowProjectSpec(workspace)
            else:
                return FlowProjectSpec(workspace, enclosing_project)
        else:
            # TODO: check the logic
            child_projects = find_child_projects(dir)
            if not len(child_projects):
                print 'bad workspace'
                sys.exit(1)
            workspace = Workspace(child_projects)
            return FlowProjectSpec(workspace)

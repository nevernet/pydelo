#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web import db
from web.utils.log import Logger
from web.models.projects import Projects
from web.utils.git import Git

from .base import Base

logger = Logger("project service")


class ProjectsService(Base):
    __model__ = Projects

    def git_clone(self, project):
        git = Git(project.checkout_dir, project.repo_url)
        git.clone()

    def git_branch(self, project):
        git = Git(project.checkout_dir, project.repo_url)
        return git.remote_branch()

    def git_tag(self, project):
        git = Git(project.checkout_dir, project.repo_url)
        return git.tag()

    def git_branch_commit_log(self, project, branch):
        git = Git(project.checkout_dir, project.repo_url)
        git.checkout_branch(branch)
        return git.log()


projects = ProjectsService()

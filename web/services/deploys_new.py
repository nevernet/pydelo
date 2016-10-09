# -*- coding:utf-8 -*-

from collections import OrderedDict
from web.models.deploys import Deploys
from web.models.projects import Projects
from web.services.projects import projects as project_service

from web.config import GIT_WORKING_FOLDER, SHELL_DIR, SHELL_DIR_DEPLOY, SHELL_DIR_ROLLBACK, PROJECT_SERVERS
import os
import sh
import hashlib


class DeploysServers(object):
    def _check_md5(self, projectDir):
        # type: (str) -> list, list
        """
        :param projectDir:
        :return:
        """
        readMe = ""
        title = ""
        files = OrderedDict()
        not_match_files = []
        with open(os.path.join(projectDir, "readme.txt"), "rb") as f:
            i = 0
            for line in f:
                line = line.strip()
                if i == 0:
                    title = line
                if i > 2:
                    l = line.split("\t")
                    files[l[0]] = l[1]
                i += 1
        for key in files.keys():
            p = os.path.join(projectDir, key)
            md5Str = files[key]

            if md5Str != self.md5_checksum(p):
                not_match_files.append(key)

        return not_match_files, files

    def md5_checksum(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def publish(self, deploy):
        """
        :type deploy: Deploys
        :rtype: str
        """

        msg = ""
        current_path = os.getcwd()

        # 创建临时目录
        temp_dir = "%s/temp/%s/" % (current_path, deploy.project_id)
        if os.path.exists(temp_dir) is False:
            os.makedirs(temp_dir)

        # unzip 文件到 临时目录
        cmd = sh.Command("unzip")
        msg = "%s\n%s" % (msg, cmd("-o", deploy.package_path, "-d", temp_dir))

        # get project directory
        project_dir = os.path.join(temp_dir, deploy.package_name[:-4])

        # get files which md5 not matched
        not_match_files, files = self._check_md5(project_dir)
        print "not match files:", not_match_files
        if len(not_match_files) > 0:
            msg += "\n".join(not_match_files)

        project = project_service.get(deploy.project_id)
        """:type: Projects"""

        if project.prefix not in PROJECT_SERVERS:
            return "未找到项目配置"

        msg += str(self.add_to_git(project_dir, project.prefix))

        # delete template directory
        rm = sh.Command("rm")
        rm("-rf", project_dir)

        return msg

    def rollback(self, deploy):
        """
                :type deploy: Deploys
                :rtype: str
                """

        msg = ""
        current_path = os.getcwd()

        project = project_service.get(deploy.project_id)
        """:type: Projects"""

        if project.prefix not in PROJECT_SERVERS:
            return "未找到项目配置"

        msg += str(self.rollback_to_git(project.prefix))

        return msg

    def add_to_git(self, project_dir, prefix, specify_shell=None):
        # type: (string, string, Deploys) -> string

        # git_working_directory = os.path.join(GIT_WORKING_FOLDER, prefix + "/")

        shell_file = specify_shell if specify_shell is not None else SHELL_DIR_DEPLOY
        shell = sh.Command(shell_file)

        www_dir = PROJECT_SERVERS[prefix]["folder"]
        git_working_directory = os.path.join(GIT_WORKING_FOLDER, PROJECT_SERVERS[prefix]["git_folder_name"] + "/")
        return shell(os.path.join(project_dir, "*"), git_working_directory, www_dir)

    def rollback_to_git(self, prefix, specify_shell=None):
        # git_working_directory = os.path.join(GIT_WORKING_FOLDER, prefix + "/")
        shell_file = specify_shell if specify_shell is not None else SHELL_DIR_ROLLBACK
        shell = sh.Command(shell_file)

        www_dir = PROJECT_SERVERS[prefix]["folder"]
        git_working_directory = os.path.join(GIT_WORKING_FOLDER, PROJECT_SERVERS[prefix]["git_folder_name"] + "/")
        return shell(git_working_directory, www_dir)


deploys_new = DeploysServers()

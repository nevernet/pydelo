# -*- coding:utf-8 -*-

from collections import OrderedDict
from web.models.deploys import Deploys
from web.models.projects import Projects
from web.services.projects import projects as project_service

from web.config import GIT_WORKING_FOLDER, SHELL_DIR
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
                print line
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
        if len(not_match_files) > 0:
            msg += "\n".join(not_match_files)

        project = project_service.get(deploy.project_id)
        """:type: Projects"""
        msg += self.add_to_git(project_dir, project.prefix)

        # delete template directory
        rm = sh.Command("rm")
        rm("-rf", project_dir)

        return msg

    def add_to_git(self, project_dir, prefix):
        # type: (string, string, Deploys) -> string

        target_directory = os.path.join(GIT_WORKING_FOLDER, prefix + "/")
        shell_file = os.path.join(SHELL_DIR, "shells/%s_deploy.sh" % (prefix))
        print shell_file
        shell = sh.Command(shell_file)
        www_dir = "/Users/qinxin/projects/github/nevernet/pydelo/www-test/admin.witretail.cn"
        print shell(os.path.join(project_dir, "*"), target_directory, www_dir)

        pass

    def rollback(self, deploy):
        """
        :type deploy: Deploys
        :rtype: str
        """
        pass


deploys_new = DeploysServers()

if __name__ == "__main__":
    temp_dir = "/Users/qinxin/projects/github/nevernet/pydelo/temp/2/"
    filename = "admin.witretail.cn.updates.201609101130.54818b6e.zip"
    pass

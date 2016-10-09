# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

# -- app config --
DEBUG = True
PORT = 9998

# -- mysql config --
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"
DB_PASS = "123"
DB_NAME = "pydelo"

# -- web app config --
# SECRET_KEY = "secret-key"
# SESSION_COOKIE_NAME = "pydelo"
# PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
# SITE_COOKIE = "pydelo-ck"

GIT_WORKING_FOLDER = "/hoem/git/git-working"
SHELL_DIR = "/root/pydelo"

SHELL_DIR_DEPLOY = "%s/shells/deploy.sh" % SHELL_DIR
SHELL_DIR_ROLLBACK = "%s/shells/rollback.sh" % SHELL_DIR

PROJECT_SERVERS = {
    "api.test.com": {  # 这里的配置必须和创建项目里的"项目文件前缀"保持一致
        "git_folder_name": "test-project",
        "folder": "/opt/www/api.test.com",
    }
}

# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

import traceback
import json
import time
import random
import string
import sys
import os
import datetime

from web.models.projects import Projects
from web.models.deploys import Deploys
from flask import g
from werkzeug.utils import secure_filename

if sys.version_info > (3,):
    string.letters = string.ascii_letters
from hashlib import md5

from web.utils.log import Logger

logger = Logger("API")

from web import app
from web.services.users import users
from web.services.hosts import hosts
from web.services.deploys import deploys
from web.services.deploys_new import deploys_new
from web.services.projects import projects
from web.utils.error import Error
from .login import authorize

from flask import request, jsonify, g


@app.errorhandler(Error)
def error(err):
    return jsonify(dict(rc=err.rc, msg=err.msg))


@app.route("/api/accounts/password", methods=["PUT"])
@authorize
def api_update_accounts():
    password = request.form.get("password")
    password = md5(password.encode("utf-8")).hexdigest().upper()
    users.update(g.user, password=password)
    return jsonify(dict(rc=0))


@app.route("/api/login", methods=["POST"])
def api_user_login():
    username = request.form.get("username")
    password = request.form.get("password")
    sign = users.login(username, password)
    return jsonify(dict(rc=0, data=dict(sign=sign)))


@app.route("/api/deploys", methods=["GET"])
@authorize
def api_deploys():
    offset = request.args.get("offset", None, type=int)
    limit = request.args.get("limit", None, type=int)

    data = {}
    count = 0

    if g.user.role == g.user.ROLE["ADMIN"]:
        data = deploys.find(offset, limit, order_by="id", desc=True)
        count = deploys.count()
        # return jsonify(dict(rc=0,
        #                     data=dict(deploys=data,
        #                               count=count)))
    else:
        data = deploys.find(offset, limit, order_by="id", desc=True,
                            user_id=g.user.id)
        count = deploys.count(user_id=g.user.id)

    new_data = []
    for p in data:
        """ :type: Deploys"""

        p1 = {}
        for k in dict(p.__dict__).keys():
            if k.startswith("_") == True:
                continue
            if k != "package_path" and k != "project" and k != "user":
                p1[k] = getattr(p, k)

        p1["updated_at"] = p1["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        p1["created_at"] = p1["created_at"].strftime("%Y-%m-%d %H:%M:%S")

        project = {
            "name": p.project.name,
        }
        user = {
            "name": p.user.name,
        }
        p1["project"] = project
        p1["user"] = user
        new_data.append(p1)

        # keys = dict(p.user.__dict__).keys()
        # # print keys
        # for k in keys:
        #     print k, k.startswith("_")
        #     if k.startswith("_") == True:
        #         continue
        #     if k != "name":
        #         del p.user.__dict__[k]

    return jsonify(dict(rc=0,
                        data=dict(deploys=new_data,
                                  count=count)))


@app.route("/api/deploys", methods=["POST"])
@authorize
def api_post_deploy():
    if "package" not in request.files:
        return jsonify(dict(rc=-1, msg="未上传文件"))

    project_id = request.args.get("project_id")
    if project_id < 1:
        return jsonify(dict(rc=-1, msg="未选择项目"))

    project = projects.get(project_id)
    """ :type: Projects"""
    if project is None:
        return jsonify(dict(rc=-1, msg="项目不存在"))

    if project.users is None:
        return jsonify(dict(rc=-1, msg="不具备该项目的权限[1]"))

    if g.user.id != 1 and project.users[0].id != g.user.id:
        return jsonify(dict(rc=-1, msg="不具备该项目的权限[2]"))

    savePath = "%s/uploads/%s/%s" % (os.getcwd(), datetime.datetime.today().strftime('%Y/%m/%d'), project_id)
    if os.path.exists(savePath) is False:
        os.makedirs(savePath, 0755)

    file = request.files["package"]
    """ :type: werkzeug.datastructures.FileStorage"""
    if file.filename == "":
        return jsonify(dict(rc=-1, msg="未上传文件1"))

    secureFilename = secure_filename(file.filename)
    saveFile = os.path.join(savePath, secureFilename)

    if secureFilename[-4:] != ".zip":
        return jsonify(dict(rc=-1, msg="文件类型必须为.zip"))

    # 文件前缀检查，避免传错项目文件
    print secureFilename[:-4], project.prefix
    if secureFilename.startswith(project.prefix) == False:
        return jsonify(dict(rc=-1, msg="项目文件前缀不符合，您可以传错文件了"))

    file.save(saveFile)

    host_id = request.args.get("host_id")
    mode = request.form.get("mode", type=int)
    tag = request.form.get("tag")
    branch = request.form.get("branch") if mode == 0 else ""
    commit = request.form.get("commit") if mode == 0 else tag
    tag = ""

    host_id = 0
    mode = 0
    branch = ""

    commit = ""

    deploy = deploys.create(
        user_id=g.user.id,
        package_name=secureFilename,
        package_path=saveFile,
        project_id=project_id,
        host_id=host_id,
        mode=mode,
        status=2,
        branch=branch,
        version=commit,
        softln_filename=time.strftime(
            "%Y%m%d-%H%M%S") + "-" + commit,
    )
    # deploys.deploy(deploy)
    return jsonify(dict(rc=0, data=dict(id=deploy.id)))


@app.route("/api/deploys/<int:id>", methods=["PUT"])
@authorize
def update_deploy_by_id(id):
    action = request.form.get("action")
    deploy = deploys.get(id)
    if action == "redeploy":
        new_deploy = deploys.create(
            user_id=deploy.user_id,
            project_id=deploy.project_id,
            host_id=deploy.host_id,
            mode=deploy.mode,
            status=2,
            branch=deploy.branch,
            version=deploy.version,
            softln_filename=deploy.softln_filename)
        deploys.deploy(new_deploy)
        return jsonify(dict(rc=0, data=dict(id=new_deploy.id)))
    elif action == "rollback":
        # new_deploy = deploys.create(
        #     user_id=deploy.user_id,
        #     project_id=deploy.project_id,
        #     host_id=deploy.host_id,
        #     mode=2,
        #     status=2,
        #     branch=deploy.branch,
        #     version=deploy.version,
        #     softln_filename=deploy.softln_filename)
        # deploys.rollback(new_deploy)

        # return jsonify(dict(rc=0, data=dict(id=new_deploy.id)))

        msg = deploys_new.rollback(deploy)
        deploys.update(deploy, **dict(deploy_status=2))
        return jsonify(dict(rc=0, msg=msg))

    elif action == "publish":
        msg = deploys_new.publish(deploy)
        deploys.update(deploy, **dict(deploy_status=1))
        return jsonify(dict(rc=0, msg=msg))
    elif action == "cancel":
        deploys.update(deploy, **dict(deploy_status=99))
        return jsonify(dict(rc=0, data=None))
    else:
        return jsonify(dict(rc=-1, msg="action is not supported"))
        # raise Error(10000, msg=None)


@app.route("/api/deploys/<int:id>", methods=["GET"])
@authorize
def get_deploy_progress_by_id(id):
    deploy = deploys.get(id)
    return jsonify(dict(rc=0, data=deploy))


# @app.route("/api/alldeploys", methods=["GET"])
# @authorize
# def api_alldeploys():
#     offset = request.args.get("offset", None, type=int)
#     limit = request.args.get("limit", None, type=int)
#     return jsonify(dict(rc=0,
#         data=dict(deploys=deploys.all(offset, limit, order_by="updated_at", desc=True),
#                   count=deploys.count())))

@app.route("/api/projects", methods=["GET"])
@authorize
def api_projects():
    offset = request.args.get("offset", None, type=int)
    limit = request.args.get("limit", None, type=int)
    data = users.get_user_projects(g.user, offset=offset, limit=limit, order_by="id", desc=True)
    return jsonify(dict(rc=0, data=data))


@app.route("/api/projects", methods=["POST"])
@authorize
def api_create_project():
    projects.create(**request.form.to_dict())
    return jsonify(dict(rc=0))


@app.route("/api/projects/<int:id>", methods=["GET"])
@authorize
def api_get_project_by_id(id):
    return jsonify(dict(rc=0, data=projects.get(id)))


@app.route("/api/projects/<int:id>", methods=["PUT"])
@authorize
def api_update_project_by_id(id):
    projects.update(projects.get(id), **request.form.to_dict())
    return jsonify(dict(rc=0))


@app.route("/api/projects/<int:id>", methods=["DELETE"])
@authorize
def api_delete_project_by_id(id):
    projects.delete(projects.get(id))
    return jsonify(dict(rc=0))


@app.route("/api/projects/<int:id>/branches", methods=["GET"])
@authorize
def api_project_branches(id):
    project = projects.get(id)
    projects.git_clone(project)
    return jsonify(dict(rc=0, data=projects.git_branch(project)))


@app.route("/api/projects/<int:id>/tags", methods=["GET"])
@authorize
def api_project_tags(id):
    project = projects.get(id)
    projects.git_clone(project)
    return jsonify(dict(rc=0, data=projects.git_tag(project)))


@app.route("/api/projects/<int:id>/branches/<branch>/commits", methods=["GET"])
@authorize
def api_project_branch_commits(id, branch):
    logger.debug("get branch commits:{0}, branch:{1}".format(id, branch))
    project = projects.get(id)
    projects.git_clone(project)
    return jsonify(dict(rc=0, data=projects.git_branch_commit_log(project, branch)))


# 获取所有hosts
@app.route("/api/hosts", methods=["GET"])
@authorize
def api_hosts():
    offset = request.args.get("offset", None, type=int)
    limit = request.args.get("limit", None, type=int)
    data = users.get_user_hosts(g.user, offset=offset, limit=limit)
    return jsonify(dict(rc=0, data=data))


# 获取某个host
@app.route("/api/hosts/<int:id>", methods=["GET"])
@authorize
def api_get_host_by_id(id):
    return jsonify(dict(rc=0, data=hosts.get(id)))


# 更新某个host
@app.route("/api/hosts/<int:id>", methods=["PUT"])
@authorize
def api_update_host_by_id(id):
    hosts.update(hosts.get(id), **request.form.to_dict())
    return jsonify(dict(rc=0))


# 新建host
@app.route("/api/hosts", methods=["POST"])
@authorize
def create_hosts():
    hosts.create(**request.form.to_dict())
    return jsonify(dict(rc=0))


@app.route("/api/users", methods=["POST"])
@authorize
def create_users():
    apikey = ''.join(random.choice(string.letters + string.digits) for _ in range(32))
    user_params = request.form.to_dict();
    user_params["password"] = md5(user_params["password"].encode("utf-8")).hexdigest().upper()
    users.create(apikey=apikey, **user_params)
    return jsonify(dict(rc=0))


@app.route("/api/users", methods=["GET"])
@authorize
def api_users():
    offset = request.args.get("offset", None, type=int)
    limit = request.args.get("limit", None, type=int)
    return jsonify(dict(rc=0, data=dict(users=users.all(offset, limit), count=users.count())))


@app.route("/api/users/<int:id>", methods=["GET"])
@authorize
def api_get_user_by_id(id):
    return jsonify(dict(rc=0, data=users.get(id)))


@app.route("/api/users/<int:id>", methods=["DELETE"])
@authorize
def api_delete_user_by_id(id):
    if int(id) == 1:
        return jsonify(dict(rc=-1, msg="权限不够"))
    users.delete(users.get(id))
    return jsonify(dict(rc=0))


@app.route("/api/users/<int:id>/hosts", methods=["GET"])
@authorize
def api_get_user_hosts_by_id(id):
    user = users.get(id)
    data = users.get_user_hosts(user)
    return jsonify(dict(rc=0, data=data))


@app.route("/api/users/<int:id>/hosts", methods=["PUT"])
@authorize
def api_update_user_hosts_by_id(id):
    user = users.get(id)
    user.hosts = []
    for host in request.form.getlist("hosts[]"):
        user.hosts.append(hosts.get(int(host)))
    users.save(user)
    return jsonify(dict(rc=0))


@app.route("/api/users/<int:id>/projects", methods=["GET"])
@authorize
def api_get_user_projects_by_id(id):
    user = users.get(id)
    data = users.get_user_projects(user)
    return jsonify(dict(rc=0, data=data))


@app.route("/api/users/<int:id>/projects", methods=["PUT"])
@authorize
def api_update_user_projects_by_id(id):
    user = users.get(id)
    user.projects = []
    for project in request.form.getlist("projects[]"):
        user.projects.append(projects.get(int(project)))
    users.save(user)
    return jsonify(dict(rc=0))

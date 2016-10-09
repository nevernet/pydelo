#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web import db
from web.utils.jsonencoder import JsonSerializer


class Deploys(JsonSerializer, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    host_id = db.Column(db.Integer, db.ForeignKey("hosts.id"))
    package_name = db.Column(db.String(200))
    package_path = db.Column(db.String(200))
    mode = db.Column(db.Integer)
    branch = db.Column(db.String(32))
    version = db.Column(db.String(32))
    progress = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    softln_filename = db.Column(db.String(64))
    comment = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deploy_status = db.Column(db.Integer, default=0)

    user = db.relationship("Users", backref=db.backref("deploys", lazy="dynamic"))
    project = db.relationship("Projects", backref=db.backref("deploys", lazy="dynamic"))
    host = db.relationship("Hosts", backref=db.backref("deploys", lazy="dynamic"))

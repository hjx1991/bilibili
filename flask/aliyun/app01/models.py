#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exts import db
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid
import datetime

class ImageModel(db.Model):
    __tablename__='img'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    img = db.Column(db.LargeBinary,nullable=False)
    img_time = db.Column(db.DATETIME,default=datetime.datetime.now())

    def __str__(self):
        return "img"

class UserModel(db.Model):
    __tablename__ = 'users'
    id =db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    telephone = db.Column(db.String(11),nullable=False)
    _password = db.Column(db.String(128),nullable=False)

    def __str__(self):
        return "users"


    # def __init__(self, *args, **kwargs):
    #     password = kwargs.pop('password')
    #     username = kwargs.pop('username')
    #     telephone = kwargs.pop('telephone')
    #     self.password = password
    #     self.username = username
    #     self.telephone = telephone

    @property
    def password(self):
        # return self.password
        # raise AttributeError('Password is not a readable attribute')
        return self._password

    @password.setter
    def password(self, rawpwd):
        self._password = generate_password_hash(rawpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self._password, rawpwd)

'''
第一次        python manage.py db init/migrate/upgrade
第二次        python manage.py db migrate/upgrade
'''
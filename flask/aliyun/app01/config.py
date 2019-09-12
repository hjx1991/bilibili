#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'aliyun'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True

SECRET_KEY  = os.urandom(24)
PERMANENT_SESSION_LIFETIME = 600
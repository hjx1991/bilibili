#-*- coding:utf-8 -*-
import os
DEBUG = True

SQLALCHEMY_DATABASE_URI =  'mysql+pymysql://root:123456@localhost:3306/aliyun?charset=utf8'

SECRET_KEY=os.urandom(24)
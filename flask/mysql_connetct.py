#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import MySQLdb

db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='aliyun')

cursor = db.cursor()
cursor.execute("select * from mysql.user")

res = cursor.fetchall()

print(res)
res = cursor.fetchone()
while res:
    print(res)
    res = cursor.fetchone()
db.close()
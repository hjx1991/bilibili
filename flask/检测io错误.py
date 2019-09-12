#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import time
import re

SAS, SSD = 'sd\S', 'nvme\d[a-z0-9A-Z]{3}'


def Cmd(cmd):
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.readlines()


def run():
    # 当前时间
    current_time = time.ctime().split()[1:]
    # current_time=['Aug', '5', '06:30:00', '2019']
    mon, day, min = current_time[0], current_time[1], current_time[2][:-3]
    # print("now time:",mon,day,min)

    # 过去5分钟时间
    old_time = time.ctime(time.time() - 300).split()[1:]
    # old_time = ['Aug', '5', '06:25:00', '2019']
    old_mon, old_day, old_min = old_time[0], old_time[1], old_time[2][:-3]
    # print("old time:",old_mon, old_day, old_min)
    # 日志文件格式：天数日期10以下为空格2个，10以上则天数空格1个如： Aug  5 06:25:00 2019|||Aug 15 06:25:00 2019
    if int(day) >= 10:
        shell_now = '%s %s %s' % (mon, day, min)
    if int(day) < 10:
        shell_now = '%s  %s %s' % (mon, day, min)
    if int(old_day) >= 10:
        shell_old = '%s %s %s' % (old_mon, old_day, old_min)
    if int(old_day) < 10:
        shell_old = '%s  %s %s' % (old_mon, old_day, old_min)
    shell = "sed -n '/%s/,/%s/p' kern.log" % (shell_old, shell_now)
    # shell = "sed -n '/Aug  5 06:30/,/Aug  5 06:35/p' kern.log.1"

    result = Cmd(shell)
    for error in result:
        if 'I/O error' in error and 'sd' in error:
            req = re.search(SAS, error)
            print("I/O error:", req.group())
            return "I/O error: %s" % req.group()
        if 'I/O error' in error and 'nvme' in error:
            req1 = re.search(SSD, error)
            print("I/O error:", req1.group())
            return "I/O error: %s" % req1.group()

if __name__ == '__main__':
    run()
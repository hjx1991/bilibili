#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
2019-7-15  Author hujunxiong
'''
import subprocess
import os
import sys
'''此脚本用于bcache环境,根据读取磁盘文件内容区分类型并格式化挂载'''
#预定义安装python3
os.system('apt-get -y install python3 python-pip --force-yes')

#备份和清理cache历史
os.system("cp /etc/fstab /data/fstab.bak; sed -i '/acache/d' /etc/fstab; sed -i '/vcache/d' /etc/fstab; sed -i '/bcache/d' /etc/fstab" )

#预定义存放盘符list
sas = []
ssd = []

#执行shell函数,返回list
def shell_return(cmd):
    req = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = req.communicate()
    information = str(out, encoding='utf-8').strip()
    result = information.split('\n')
    return result

#执行并接受shell函数的返回值进行处理
def shell_result():
    foreclose_root ="fdisk -l 2>/dev/null|grep Disk|grep -Ev 'ident|label|loop|mapper'|grep -v `df -h|awk '{if($NF~/^\/$/) print $1}'|cut -b 1-8`|awk '{print $2,$5}'|awk -F: '{print $1}'|sort"
    result = shell_return(foreclose_root)
    for disk in result:
        drive = disk.split('/')
        file_name ='cat /sys/block/%s/queue/rotational'% drive[2]
        disk_result = shell_return(file_name)
        if int(disk_result[0]) == 1:
            sas.append(disk)
        if int(disk_result[0]) == 0:
            ssd.append(disk)

class disk_init:
    def __init__(self):
        self.LOAD_XFS = 'modprobe xfs'
        self.ssd = 'mkfs.xfs -f -i size=512,attr=2 -l version=2,size=128m -d su=64k,sw=1'
        self.sas = 'mkfs.xfs -f -i size=512,attr=2 -l version=2,size=128m -d su=64k,sw=10'
    def sas_disk(self):
        try:
            sas.sort()
            os.system(self.LOAD_XFS)
            '''格式化'''
            for disk in sas:
                os.system('%s %s' % (self.sas,disk))
            num = len(sas)
            for n in range(num):
                if n >= 10:
                    result = os.system("mkdir -p /data/bcache/L3/disk%d && mount -t xfs %s /data/bcache/L3/disk%d && echo '/data/bcache/L3/disk%d' >/data/bcache/L3/disk%d/info" % (n, sas[n], n,n,n))
                if n <10:
                    result = os.system("mkdir -p /data/bcache/L3/disk0%d && mount -t xfs %s /data/bcache/L3/disk0%d && echo '/data/bcache/L3/disk0%d' >/data/bcache/L3/disk0%d/info" % (n,sas[n],n,n,n))

        except Exception as e:
            print(e)
            sys.exit()

    def ssd_disk(self):
        if len(ssd) == 0:
            return "No SSD disks"
        try:
            os.system(self.LOAD_XFS)
            ssd.sort()
            '''格式化'''
            for disk in ssd:
                os.system('%s %s' % (self.ssd, disk))
            num = len(ssd)
            for n in range(num):
                result = os.system("mkdir -p /data/bcache/L2/disk0%d && mount -t xfs %s /data/bcache/L2/disk0%d && echo '/data/bcache/L2/disk0%d'>/data/bcache/L2/disk0%d/info" % (n, ssd[n], n,n,n))
        except Exception as e:
            print(e)
            sys.exit()

if __name__ == '__main__':
    shell_result()
    bili=disk_init()
    bili.sas_disk()
    bili.ssd_disk()

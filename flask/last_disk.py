#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
2019-7-5  Author hujunxiong
'''
import subprocess
import os
import sys
'''此脚本用于bcache环境 根据磁盘容量区分并挂载'''
#预定义安装python3
os.system('apt-get install -y  python3-pip python3 packagename')

#备份和清理acache和vcache历史
os.system("cp /etc/fstab /data/fstab.bak && sed -i '/acache/d' /etc/fstab &&sed -i '/vcache/d' /etc/fstab " )

sas = []
ssd = []
dict_disk={}

'''函数执行命令获取fdisk所有磁盘信息并排除/目录，生成有序sas、ssd列表'''
def shell_result():
    foreclose_root ="fdisk -l 2>/dev/null|grep Disk|grep -Ev 'ident|label|loop|mapper'|grep -v `df -h|awk '{if($NF~/^\/$/) print $1}'|cut -b 1-8`|awk '{print $2,$5}'|awk -F: '{print $1,$2}'|sort"
    sda = subprocess.Popen(foreclose_root, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = sda.communicate()
    information = str(out, encoding='utf-8').strip()
    all_disk = information.split('\n')
    for connect in all_disk:
        if len(connect) <30:
            dict_disk[connect.split()[0]]=connect.split()[1]
    for drive,byte in dict_disk.items():
        capacity = int(byte)/1024/1024/1024/1024
        #小于1.5T为SSD硬盘
        if capacity <1.5:
            ssd.append(drive)
        else:
            sas.append(drive)

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
                if '/dev/sd' in disk:
                    os.system('%s %s' % (self.sas,disk))
            num = len(sas)
            for n in range(num):
                if n >= 10:
                    result = os.system("mkdir -p /data/bcache/L3/disk%d && mount -t xfs %s /data/bcache/L3/disk%d && echo '/data/bcache/L3/disk%d' >/data/bcache/L3/disk%d/info" % (n, sas[n], n,n,n))
                result = os.system("mkdir -p /data/bcache/L3/disk0%d && mount -t xfs %s /data/bcache/L3/disk0%d && echo '/data/bcache/L3/disk0%d' >/data/bcache/L3/disk0%d/info" % (n,sas[n],n,n,n))

        except Exception as e:
            print(e)
            sys.exit()

    def ssd_disk(self):
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
#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import datetime
os.system('cp /etc/fstab /data/fstab.bak')
sas = []
ssd = []
#分区:UUID
ssd_kv = {}
sas_kv = {}
sas_list=[]
ssd_list=[]
data = datetime.datetime.now().strftime('%Y-%m-%d')
'''本脚本只对没挂载的磁盘进行初始化磁盘挂载,已挂载的目录先手动umount'''

class bcache_disk_init:
    '''载入变量'''
    def __init__(self):
        self.cmd = 'blkid'
        self.req = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.out, self.err = self.req.communicate()
        self.information = str(self.out, encoding='utf-8').strip()
        self.information_str_list = self.information.split('\n')
        self.LOAD_XFS = 'modprobe xfs'
        self.ssd = 'mkfs.xfs -f -i size=512,attr=2 -l version=2,size=128m -d su=64k,sw=1'
        self.sas = 'mkfs.xfs -f -i size=512,attr=2 -l version=2,size=128m -d su=64k,sw=10'

    def sas_disk(self):
        try:
            os.system(self.LOAD_XFS)
            for disk in self.information_str_list:
                disk_list = disk.split(' ')
                '''disk_list =['/dev/nvme0n1:','UUID=xx','TYPE="xfs"'] 系统盘多项PARTUUID'''
                if len(disk_list) < 4 and '/dev/sd' in disk_list[0]:
                    '''加入字典作写入fstab'''
                    sas_kv[disk_list[0][:-1]] = disk_list[1]   #剪切:
                    '''添加list作排序'''
                    sas.append(disk_list[0][:-1])
                    '''格式化'''
                    os.system('%s %s' % (self.sas, disk_list[0][:-1]))
            sas.sort()
            num = len(sas)
            '''创建目录并挂载磁盘'''
            for n in range(num):
                result = os.system('mkdir -p /data/bcache/L3/disk0%d && mount -t xfs %s /data/bcache/L3/disk0%d' % (n,sas[n],n))
                if result != 0:
                    print('mkdir -p /data/bcache/L3/disk0%d && mount -t xfs %s /data/bcache/L3/disk0%d' % (n,sas[n],n))
                sas_list.append('/data/bcache/L3/disk0%d' % n)
                if n >= 10:
                    result = os.system('mkdir -p /data/bcache/L3/disk%d && mount -t xfs %s /data/bcache/L3/disk%d' % (n, sas[n], n))
                    if result != 0:
                        print('mkdir -p /data/bcache/L3/disk0%d && mount -t xfs %s /data/bcache/L3/disk0%d' % (n, sas[n], n))
        except Exception as e:
            print(e)
            sys.exit()

    def ssd_disk(self):
        try:
            os.system(self.LOAD_XFS)
            for disk in self.information_str_list:
                disk_list = disk.split(' ')
                '''disk_list =['/dev/nvme0n1:','UUID=xx','TYPE="xfs"'] 系统盘多项PARTUUID'''
                if len(disk_list) and'/dev/nvme' in disk_list[0]:
                    '''加入字典作写入fstab'''
                    ssd_kv[disk_list[0][:-1]] = disk_list[1]
                    '''添加list作排序'''
                    ssd.append(disk_list[0][:-1])
                    print(ssd_kv,ssd)
                    '''格式化'''
                    result = os.system('%s %s' % (self.ssd, disk_list[0][:-1]))
                    if result != 0:
                        print('%s %s' % (self.ssd, disk_list[0][:-1]))
            ssd.sort()
            num = len(ssd)
            for n in range(num):
                print('mount:',n,ssd[n], n)
                result = os.system('mkdir -p /data/bcache/L2/disk0%d && mount -t xfs %s /data/bcache/L2/disk0%d' % (n,ssd[n], n))
                if result != 0:
                    print('mkdir -p /data/bcache/L2/disk0%d && mount -t xfs %s /data/bcache/L2/disk0%d' % (n, ssd[n],n))
                ssd_list.append('/data/bcache/L2/disk0%d'%n)
        except Exception as e:
            print(e)
            sys.exit()
    def echo_fstab(self):
        os.system('echo #%s >> /etc/fstab' % data)


if __name__ == '__main__':

    hjx =bcache_disk_init()
    hjx.sas_disk()
    hjx.ssd_disk()

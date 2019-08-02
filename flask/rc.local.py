#!/bin/bash
#author hujunxiong 2019-7-8
mkdir /tmp/test
test_dir="/tmp/test"
root=`df -h|awk '{if($NF~/^\/$/) print $1}'|cut -b 1-8`
list=`fdisk -l|grep Disk|grep dev|grep -v ${root}|awk '{print $2}'|awk -F: '{print $1}'`
for disk in ${list}
do
echo ${disk}
 mount -t xfs ${disk}  ${test_dir}
 mount_point=`cat ${test_dir}/info`
 umount ${test_dir}
 mkdir -p ${mount_point}
 mount -t xfs ${disk}  ${mount_point}
done
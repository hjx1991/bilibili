#!/usr/bin/env python
import os,sys
import time
import shutil
import subprocess
import socket
#author:yuyachao
#build:20181126
#settings
bakdir='/data/netconfig.bak'
configfile='/etc/network/interfaces'
restarteth='systemctl restart networking.service'


def SubprocessCaller(cmd):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = p.communicate()
    except OSError as e:
        print('SubprocessCaller function: execute command failed, message is %s' % e)
        return dict(output=[], error=[], code=1)
    else:
        return dict(output=output, error=error, code=0)

def FileWalk(configdir):
    result = {'dir': {}, 'file': {}, 'dirfile': {}}
    if not os.path.exists(configdir):
        print('%s not exists' % configdir)
        return {}

    for dirpath, dirnames, filenames in os.walk(configdir):
        if len(dirnames) > 0:
            result['dir'][dirpath] = dirnames
        if len(filenames) > 0:
            result['dirfile'][dirpath] = filenames
            for file in filenames:
                filefullpath = os.path.join(dirpath, file)
                try:
                    result['file'][filefullpath] = file.split('-')[-1]
                except:
                    pass
    return result.get('file')

def configBackup(oldconfig):
    if not os.path.exists(bakdir):
        os.makedirs(bakdir)
        oldfilename=configfile.split(os.sep)[-1]
        bakfile=bakdir+str(oldfilename)
    if os.path.exists(bakfile):
        timest=int(time.time())
        bakfile=bakfile+'-'+str(timest)
    try:
        shutil.copy(oldconfig,bakfile)
    except Exception as e:
        sys.exit(2000)

def goBack():
    backlist=FileWalk(bakdir)
    if len(backlist)>0:
        sortlist={value:key for key,value in backlist.items()}
        latestkey=sorted(sortlist.keys())[-1]
        bakf=sortlist.get(latestkey)
    else:
        bakf=bakdir+str(configfile.split(os.sep)[-1])
    if bakf:
        shutil.move(configfile,'/tmp')
        shutil.copy(bakf,configfile)

def getGateway():
    gr="/sbin/route -n  |grep -v -E '^[A-Za-z]'|awk '{if($1==\"0.0.0.0\")print $0}'"
    res=SubprocessCaller(gr)
    if res['code'] == 0 and not res['error']:
        r={}
        for i in res.get('output').split('\n'):
            try:
                r[i.split()[-1]]=i.split()
                dr=i.split()[-1]
            except:
                pass
        if len(r)==1:
            gw=r[dr][1]
            return gw
        else:
            return

def pingTest(ip):
    ping="ping -c 2 %s|| echo 'fail' "%ip
    res=SubprocessCaller(ping)
    if res['code'] == 0 and not res['error']:
        if res.get('output') != 'fail':
            return True
    else:
        return False

def writeConfigs(address,netmask,gateway,ethname='bond0'):
    configBackup(configfile)
    configinfo='iface %s inet6 static \naddress %s\nnetmask %s\nup route -A inet6 add default gw %s dev %s\n'%(ethname,address,netmask,gateway,ethname)
    try:
        f=open(configfile,'a')
        f.write(configinfo)
        f.close()
    except Exception as e:
        print(e)
        goBack()

    res=SubprocessCaller(restarteth)
    if res['code'] == 0 and not res['error']:
        gw=getGateway()
        if gw:
            if pingTest(gw):
                print('add ipv6 ok')
            else:
                goBack()
                SubprocessCaller(restarteth)
        else:
            goBack()
            SubprocessCaller(restarteth)
    else:
        goBack()
        SubprocessCaller(restarteth)



def getConfigs():
    configs = {}
    res=None
    try:
        configs['address'] =sys.argv[1]
        configs['netmask'] =sys.argv[2]
        configs['gw']=sys.argv[3]
        configs['hostname']=sys.argv[4]
        return configs
    except Exception as e:
        print(e)
        sys.exit()

def envCheck():
    envcheck="awk '/disable_ipv6/{print $0}' /etc/sysctl.conf "
    res=SubprocessCaller(envcheck)
    if res['code'] == 0 and not res['error']:
        for info in res.get('output').split('\n'):
            if len(info.split('='))>1:
                if info.split('=')[-1].strip() != "0":
                    print("%s error,please check!!"%info)
                    sys.exit(2000)

if __name__=="__main__":
    envCheck()
    configs=getConfigs()
    print(configs.get('address'),configs.get('netmask'),configs.get('gw'))
    writeConfigs(configs.get('address'),configs.get('netmask'),configs.get('gw'))


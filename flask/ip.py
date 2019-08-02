#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess


cmd = "curl -v 'http://octopus.bilibili.co/api/v1/octopus/load_balance/list?pageNum=1&pageSize=999' -H \"Cookie:cp=1; _AJSESSIONID=0544372954a2f0a8c97c67752f7f7757; username=shichengxiang; _gitlab_session=430acd4877ad724ddef55de083f3fe43; event_filter=all; session=c748d2ac6ee178c06ef94610ecf88915\" | jq ."

req = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

out,err = req.communicate()
print(out)
out_info = str(out,encoding='utf-8')

print(out_info)



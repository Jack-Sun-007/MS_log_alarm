# -*- coding: utf-8 -*-
import os
import codecs
import datetime
import requests
import json

#定义发送钉钉报警的函数
def send_msg(text,mobile):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    json_text = {
                "msgtype": "text",
                "text": {
                    "content": text
                },
                "at": {
                    "atMobiles": [
                        mobile
                    ],
                    "isAtAll": False
                }
            }
    requests.post(url, json.dumps(json_text), headers=headers).content

#钉钉联系人
abc = "\"130xxxxxxxx\""

#获取当天日期和时间
time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:")
date1 = datetime.datetime.now().strftime("%Y-%m-%d")

#读取当天log日志文件路径
p = 'C:\\Thermo\\Instruments\\Exploris\\2.0\\System\\Programs\\dependencies\\logs\\'
for filename in os.listdir(p):
        value = os.path.join(p,filename)
        if date1 in value:
            path = value

#打开log文件，获取每行日志信息至lines，并关闭log文件
with open(path, 'r', encoding='utf_8_sig') as fp:
    lines = fp.readlines()
fp.close()

#读取1小时内log文件中的ERROR和WARNING信息
error_text = "480\n[**ERROR**]\n"
warning_text = "480\n[***WARNING***]\n"
for line in lines:
    if time1 in line:
        if "=WARN" in line:
            text = line[line.rfind("{level}"):]
            warning_text = warning_text + text
        if "=ERROR" in line:
            text = line[line.rfind("{level}"):]
            error_text = error_text + text

#如果日志出现报警就发送钉钉提醒
if len(error_text) > 30:
    print(error_text)
    send_msg(error_text, abc)
if len(warning_text) > 30:
    print(warning_text)
    send_msg(warning_text, abc)
fp.close()
# -*- coding: utf-8 -*-
import codecs
import re
import datetime
import requests
import json
import time

#获取前1小时的日期和时间
time1= (datetime.datetime.now()+datetime.timedelta(seconds=-3600)).strftime("%Y-%m-%d %H:")

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

#打开log文件，获取每行日志信息至lines，并关闭log文件
with open('C:\\Xcalibur\\system\\Exactive\\log\\Thermo Exactive--2020-09-01--12-48-15.log', 'r', encoding='utf_8_sig') as fp:
    lines = fp.readlines()
fp.close()

#读取1小时内log文件中的ERROR和WARNING信息
error_text = "QE\n[**ERROR**]\n"
warning_text = "QE\n[***WARNING***]\n"
for line in lines:
    if time1 in line:
        if "error" in line:
            text = re.sub(u"\\[.*?]", "", line)
            error_text = error_text + text
        if "warning" in line:
            text = re.sub(u"\\[.*?]", "", line)
            warning_text = warning_text + text

#如果日志出现报警就发送钉钉提醒
for line in lines:
    if time1 in line:
        if "error" in line:
            print(error_text)
            send_msg(error_text, abc)
        if "warning" in line:
            print(warning_text)
            send_msg(warning_text, abc)
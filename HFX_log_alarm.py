# -*- coding: utf-8 -*-
import codecs
import re
import datetime
import requests
import json
import time
import os

#获取前1小时的日期和时间
time1= (datetime.datetime.now()+datetime.timedelta(seconds=-3600)).strftime("%Y-%m-%d %H:")

#将log文件按时间进行排序
def get_log_list(file_path):
    dir_list = os.listdir(file_path)
    log_list = []
    if not dir_list:
        return
    else:
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse = True)
        for file in dir_list:
            if "Thermo Exactive--" in file:
                log_list.append(file)
        log_path = file_path + log_list[0]
        return log_path

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
p = get_log_list("C:\\Xcalibur\\system\\Exactive\\log\\")
with open(p, 'r', encoding='utf_8_sig') as fp:
    lines = fp.readlines()
fp.close()

#读取1小时内log文件中的ERROR和WARNING信息
error_text = "HFX\n[**ERROR**]\n"
warning_text = "HFX\n[***WARNING***]\n"
for line in lines:
    if time1 in line:
        if "error" in line:
            text = re.sub(u"\\[.*?]", "", line)
            error_text = error_text + text
        if "warning" in line:
            text = re.sub(u"\\[.*?]", "", line)
            warning_text = warning_text + text

#如果日志出现报警就发送钉钉提醒
if len(error_text) > 25:
    print(error_text)
    send_msg(error_text, abc)
if len(warning_text) > 25:
    print(warning_text)
    send_msg(warning_text, abc)

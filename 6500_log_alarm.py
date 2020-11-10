# -*- coding: utf-8 -*-
import mmap
import contextlib
import re
import requests
import json
import datetime
import time

from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view
from xml.dom import minidom

#获取前1小时的日期和时间（日志时间是+0时区）
time1= (datetime.datetime.now()+datetime.timedelta(hours=-9)).strftime("%Y-%m-%d %H:")

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

error_info="6500质谱ERROR信息：\n"
with open('C:\\Windows\\System32\\winevt\\Logs\\Application.evtx', 'r') as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
        fh = FileHeader(buf, 0)
        for xml, record in evtx_file_xml_view(fh):
            # 得到文档对象
            dom = minidom.parseString(xml)
            # 得到元素对象
            element = dom.documentElement
            # 获得子标签
            timeElement = element.getElementsByTagName("TimeCreated")
            # 获得子标签属性值
            Time = timeElement[0].getAttribute("SystemTime")
            if time1 in str(Time):
                nameElement = element.getElementsByTagName("Provider")
                name = nameElement[0].getAttribute("Name")
                if name == "Analyst":
                    error = element.getElementsByTagName("Level")[0].firstChild.data
                    if error == "2":
                        EventID = element.getElementsByTagName("EventID")[0].firstChild.data
                        if EventID == "43":
                            error_info = (error_info + "\n仪器报错但无信息\n")
                        else:
                            dataElement = element.getElementsByTagName("Data")
                            dataInfo = dataElement[0].firstChild.data
                            info = re.sub(r'<[^>]+>', '', dataInfo)
                            error_info = (error_info + info)
f.close()
print(len(error_info))
if len(error_info) > 23:
    print(error_info)
    send_msg(error_info, abc)
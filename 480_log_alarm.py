# -*- coding: utf-8 -*-
import os
import json
import time
import datetime
import requests


# 定义发送钉钉报警的函数
def send_msg(text, mobile):
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


# 钉钉联系人
def person():
    who = "\"132xxxxxxxx\""
    return who


# 读取当天log日志文件路径
def get_log_path():
    date1 = datetime.datetime.now().strftime('%Y-%m-%d')
    p = 'C:\\Thermo\\Instruments\\Exploris\\2.0\\System\\Programs\\dependencies\\logs\\'
    for filename in os.listdir(p):
        value = os.path.join(p, filename)
        if date1 in value:
            return value


# 获取日期时间戳
def get_time_stamp(log_time):
    time_array = time.strptime(log_time, '%Y-%m-%d %H:%M:%S')
    time_stamp = float(time.mktime(time_array))
    return time_stamp


# 读取log文件，按照日期分列
def get_log_info():
    with open(get_log_path(), 'r', encoding='utf_8_sig') as fp:
        txt = fp.read()
    line = txt.split('[')
    return line[1:]


# 读取60分钟内log文件中的ERROR和WARNING信息
def get_main_info():
    warning, error = set(), set()  # 定义集合筛选重复报错信息
    for i in get_log_info():
        delta_minute = (time.time() - get_time_stamp(i[0:19])) / 60
        if delta_minute <= 60:  # 60分钟内的日志筛选
            text = i[i.rfind('{msg}='):]
            if '=WARN' in i:
                if 'Opening stream from IStorage' in i:  # 筛选了无关报错信息，未找到报错原因
                    pass
                else:
                    warning.add(text)
            if '=ERROR' in i:
                error.add(text)
    return warning, error


# 如果日志出现报警就发送钉钉提醒
def main():
    warning_text = 'Orbitrap Exploris 480\n[***WARNING***]\n'
    error_text = 'Orbitrap Exploris 480\n[**ERROR**]\n'
    for a in get_main_info()[0]:
        warning_text += a
    for b in get_main_info()[1]:
        error_text += b
    if len(warning_text) > 45:
        print(warning_text)
        send_msg(warning_text, person())
    if len(error_text) > 45:
        print(error_text)
        send_msg(error_text, person())


if __name__ == '__main__':
    main()

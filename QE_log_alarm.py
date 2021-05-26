# -*- coding: utf-8 -*-
import os
import json
import time
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


# 将log文件按最后修改时间进行排序，并选择时间最新的文件
def get_log_list(file_path):
    dir_list = os.listdir(file_path)
    log_list = []
    if not dir_list:
        return
    else:
        dir_list = sorted(dir_list,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)), reverse=True)
        for file in dir_list:
            if 'Thermo Exactive--' in file:
                log_list.append(file)
        log_path = file_path + log_list[0]
        return log_path


# 获取日期时间戳
def get_time_stamp(log_time):
    time_array = time.strptime(log_time, "%Y-%m-%d %H:%M:%S")
    time_stamp = float(time.mktime(time_array))
    return time_stamp


# 读取log文件，按照日期分列
def get_log_info():
    p = get_log_list('C:\\Xcalibur\\system\\Exactive\\log\\')
    with open(p, 'r', encoding='utf_8_sig') as fp:
        txt = fp.read()
    line = txt.split('[Time=')
    return line[1:]


# 读取60分钟内log文件中的ERROR和WARNING信息
def get_main_info():
    error_text = 'Q-Exactive \n[**ERROR**]\n'
    warning_text = 'Q-Exactive \n[***WARNING***]\n'
    for i in get_log_info():
        delta_minute = (time.time() - get_time_stamp(i[0:19])) / 60
        if delta_minute <= 60:  # 60分钟内的日志筛选
            text = i[i.rfind('[Type='):]
            if 'error' in i:
                error_text += text
            if 'warning' in i:
                warning_text += text
    return warning_text, error_text


# 如果日志出现报警就发送钉钉提醒
def main():
    warning_text = get_main_info()[0]
    error_text = get_main_info()[1]
    if len(warning_text) > 40:
        print(warning_text)
        send_msg(warning_text, person())
    if len(error_text) > 40:
        print(error_text)
        send_msg(error_text, person())


if __name__ == '__main__':
    main()

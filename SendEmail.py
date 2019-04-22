#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import os
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

#发送邮箱选的163邮箱
sender = 'xlth1947@163.com'
#开启服务的时候填写的验证码
password = 'Xing2345NANjk'
# 测试
# receiver = 'zhaoxingnan@youtil.cn'
# 线上
receiver = '596142737@qq.com,zhaoxingnan@youtil.cn'
smtpserver = 'smtp.163.com'

#文件路径
# result_dir="/Users/sierra/Desktop/base/JmeterTest/report/html/"
#
# result_dir = "file:///Users/sierra/Desktop/TestReport201903040250.html"


def __sendEmial__(result_dir):
    msg = MIMEMultipart()
    # msg = MIMEText('This is just a test !', 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Python Test'

    msg.attach(MIMEText('Hi,this is the latest Automated Test Results for Youtil api!', 'plain', 'utf-8'))

    l=os.listdir(result_dir)
    #为了获取目录下时间最新的文件
    l.sort(key=lambda fn: os.path.getmtime(result_dir+"/"+fn) if not os.path.isdir(result_dir+"/"+fn) else 0)
    htmlpath2=result_dir+l[-1]#该文件路径
    print l[-1]
    #
    # # l1=os.listdir(result_dir1)
    # # #为了获取目录下时间最新的文件
    # # l1.sort(key=lambda fn: os.path.getmtime(result_dir1+"/"+fn) if not os.path.isdir(result_dir1+"/"+fn) else 0)
    # # htmlpath4=result_dir1+l1[-1]#该文件路径
    #
    att=MIMEText(open(htmlpath2,'rb').read(),'base64','utf-8')
    att["Content-Type"]='application/octet-stream'
    att["Content-Disposition"]='attachment; filename="LatestResult.html"'
    msg.attach(att)

    server = smtplib.SMTP(smtpserver,25)
    server.set_debuglevel(1)
    server.login(sender,password)
    server.sendmail(sender,receiver.split(','),msg.as_string())
    server.quit()


if __name__ == '__main__':
    __sendEmial__('')
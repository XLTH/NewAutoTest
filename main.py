#!/usr/bin/python
#  -*- coding: utf-8 -*-

import Search
import DingTalkRbot
import SendEmail

# path="file:///D:/JmeterTest/report/html/"
# result_dir="D:/JmeterTest/report/html/"

path="file:///usr/local/JmeterTest/report/html/"
result_dir="/usr/local/JmeterTest/report/html/"


webhook = "https://oapi.dingtalk.com/robot/send?access_token=90a534c1b1f603f7dca23490156f07a4b83276ff51953ee82393c5d02f773903"


eNub = int(Search.__search__(path,result_dir)[0])
resultfile = str(Search.__search__(path,result_dir)[1])

if eNub != 0:
	# print DingTalkRbot.DtalkRobot(webhook).sendText(resultfile, False, [""])
	DingTalkRbot.DtalkRobot(webhook).sendText(resultfile, False, [""])
	SendEmail.__sendEmial__(result_dir)
else:
	print "There is no error"

#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import urllib2
import json
import os


# 自定义机器人的封装类
class DtalkRobot(object):
	"""docstring for DtRobot"""
	webhook = ""

	def __init__(self, webhook):
		super(DtalkRobot, self).__init__()
		self.webhook = webhook

	# text类型
	def sendText(self, msg, isAtAll=False, atMobiles=[]):
		data = {"msgtype": "text", "text": {"content": msg}, "at": {"atMobiles": atMobiles, "isAtAll": isAtAll}}
		return self.post(data)

	# markdown类型
	def sendMarkdown(self, title, text):
		data = {"msgtype": "markdown", "markdown": {"title": title, "text": text}}
		return self.post(data)

	# link类型
	def sendLink(self, title, text, messageUrl, picUrl=""):
		data = {"msgtype": "link", "link": {"text": text, "title": title, "picUrl": picUrl, "messageUrl": messageUrl}}
		return self.post(data)

	# ActionCard类型
	def sendActionCard(self, actionCard):
		data = actionCard.getData();
		return self.post(data)

	# FeedCard类型
	def sendFeedCard(self, links):
		data = {"feedCard": {"links": links}, "msgtype": "feedCard"}
		return self.post(data)

	def post(self, data):
		post_data = json.JSONEncoder().encode(data)
		print post_data
		req = urllib2.Request(self.webhook, post_data)
		req.add_header('Content-Type', 'application/json')
		content = urllib2.urlopen(req).read()
		return content


# ActionCard类型消息结构
class ActionCard(object):
	"""docstring for ActionCard"""
	title = ""
	text = ""
	singleTitle = ""
	singleURL = ""
	btnOrientation = 0
	hideAvatar = 0
	btns = []

	def __init__(self, arg=""):
		super(ActionCard, self).__init__()
		self.arg = arg

	def putBtn(self, title, actionURL):
		self.btns.append({"title": title, "actionURL": actionURL})

	def getData(self):
		data = {"actionCard": {"title": self.title, "text": self.text, "hideAvatar": self.hideAvatar,
							   "btnOrientation": self.btnOrientation, "singleTitle": self.singleTitle,
							   "singleURL": self.singleURL, "btns": self.btns}, "msgtype": "actionCard"}
		return data


# FeedCard类型消息格式
class FeedLink(object):
	"""docstring for FeedLink"""
	title = ""
	picUrl = ""
	messageUrl = ""

	def __init__(self, arg=""):
		super(FeedLink, self).__init__()
		self.arg = arg

	def getData(self):
		data = {"title": self.title, "picURL": self.picUrl, "messageURL": self.messageUrl}
		return data


# 文件路径
# result_dir="D:/JmeterTest/report/html/"
#
# l=os.listdir(result_dir)
# #为了获取目录下时间最新的文件
# l.sort(key=lambda fn: os.path.getmtime(result_dir+"/"+fn) if not os.path.isdir(result_dir+"/"+fn) else 0)
# htmlpath2=result_dir+l[-1]#该文件路径
# print l[-1]


# 测试
# webhook = "https://oapi.dingtalk.com/robot/send?access_token=90a534c1b1f603f7dca23490156f07a4b83276ff51953ee82393c5d02f773903"
# if __name__ == "__main__":
# 	robot = DtalkRobot(webhook)
#
# 	# print robot.sendText( "现在时间：["+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"]", False, [""])
# 	# print robot.sendLink("link类型", "link类型内容link类型内容link类型内容link类型内容link类型内容link类型内容link类型内容", "http://www.baidu.com","http://scimg.jb51.net/allimg/160716/103-160G61012361X.jpg")
# 	# print robot.sendMarkdown("markdown类型", "## 标题2 \n##### 标题3 \n* 第一 \n* 第二 \n\n[链接](http://www.baidu.com/) \n")
# 	print robot.sendText(htmlpath2, False, [""])
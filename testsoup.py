#!/usr/bin/python
#  -*- coding: utf-8 -*-

import os
import re, urllib2
from bs4 import BeautifulSoup

import DingTalkRbot
import SendEmail

# 线上
# path = "file:///usr/local/JmeterTest/report/html/"
# result_dir = "/usr/local/JmeterTest/report/html/"

# test
path = "file:///Users/sierra/Desktop/LatestResult.html"
result_dir = "/Users/sierra/Desktop"


# test = "file:///Users/sierra/Desktop/TestReport201812130437.html"
# path = "file:///usr/local/JmeterTest/report/html/"
# 线上
# webhook = "https://oapi.dingtalk.com/robot/send?access_token=68b6bdd18c3838761e23d9240b26fbf1a5619a03d79b81919988fd88c3e4eee0"
# 测试
webhook = "https://oapi.dingtalk.com/robot/send?access_token=90a534c1b1f603f7dca23490156f07a4b83276ff51953ee82393c5d02f773903"

#
# l=os.listdir(result_dir)
# #为了获取目录下时间最新的文件
# l.sort(key=lambda fn: os.path.getmtime(result_dir+"/"+fn) if not os.path.isdir(result_dir+"/"+fn) else 0)
# # print l
# htmlpath=path+l[-1]#html网页文件
# htmlpath2=result_dir+l[-1]#该文件路径
#
# print htmlpath2,htmlpath


def getHtml(url):
    request = urllib2.Request(url)
    # 用进行访问地址，并且返回网页源码
    response = urllib2.urlopen(request)
    # 把网页源码转成utf-8访问
    content = response.read().decode('utf-8')
    return content


def parse(content):
    soup = BeautifulSoup(content, 'html.parser')

    failureList = soup.find_all('div', attrs={'class': 'failure'})
    successList= soup.find_all('div',attrs={'class': 'success'})
    # print failureList,successList

    # 失败接口
    if len(failureList) > 0:
        # SendEmail.__sendEmial__(result_dir)
        for failure in failureList:
            msgData = ''
            name = failure.text
            msgData = msgData + name
            # 拿父的div detail
            detailLi = failure.parent
            detail = detailLi.find('div', attrs={'class': 'detail'})
            if detail is not None:
                # 拿table 拿URL
                tableList = detail.find_all('table')
                if tableList is not None:
                    for table in tableList:
                        # print table
                        # 拿url
                        url = table.find('pre', attrs={'class': 'data'})
                        if url is not None:
                            url = url.text
                            msgData = msgData + url
                        else:
                            pass
                            # 拿td的最后一个
                        td = table.find_all('td')
                        if td is not None:
                            msg = td[len(td) - 1].text
                            tms = td[8].text
                            msgData = msgData + msg + '\n'
                            msgData = msgData + tms + '\n'
                        else:
                            pass
                    # 钉钉机器人
                    DingTalkRbot.DtalkRobot(webhook).sendText(msgData, False, [""])
                    # print msgData
                else:
                    pass
    else:
        pass

    if successList is not None:
        for success in successList:
            msgData = ''
            name = success.text
            msgData = msgData + name + '\n'
            # print MsgData
            detailLi = success.parent
            #拿时间
            tdlist = detail.find_all('td',attrs={'class': 'data key'})
            #拿时间节点的邻节点
            stm = tdlist[2]
            stm1 = stm.next_sibling
            # 拿时间节点并获取相对应的tag的值
            stms = stm1.next_sibling.get_text()
            # 转换格式
            stms = stms.encode('unicode-escape').decode('string_escape')
            #拿相应的时间值
            ms = re.compile(r'\d+').findall(stms)
            #转换为数字
            ms = int(ms[0])
            if ms >= 150:
                ms = str(ms) + 'ms'
                msgData = msgData + ms

                detail = detailLi.find('div', attrs={'class': 'detail'})
                if detail is not None:
                    tableList = detail.find_all('table')

                    for table in tableList:
                        # 拿url
                        url = table.find('pre', attrs={'class': 'data'})

                        if url is not None:
                            url = url.text
                            msgData = msgData + url + '\n'
                            # print msgData
                            #钉钉机器人
                            # DingTalkRbot.DtalkRobot(webhook).sendText(msgData, False, [""])


if __name__ == '__main__':
    html = getHtml(path)
    parse(html)


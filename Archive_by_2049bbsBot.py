import telebot
from datetime import datetime
import time
import urllib.parse
from archivenow import archivenow

import subprocess
import random
import csv

import requests
from bs4 import BeautifulSoup
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor

import warnings
warnings.filterwarnings("ignore")

bot = telebot.TeleBot("TOKEN", threaded=False)


@bot.message_handler(
    regexp="(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])")
def echo_all(message):

    # 某些微信链接包含个人独特id，有泄露隐私风险
    if message.text.startswith('https://mp.weixin.qq.com/') and '__biz=' in message.text:
        url = '&'.join(message.text.split('&', 5)[:5])
    else:
        url = message.text

    # 抓取网页
    headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3835.0 Safari/537.36",
                  "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "Accept-Language" : "en-us",
                  "Connection" : "keep-alive",
                  "Accept-Charset" : "utf-8;q=0.7,*;q=0.7"}
    html = requests.get(url, headers = headers)
    soup = BeautifulSoup(html.text, "html.parser")


    if url.startswith('https://mp.weixin.qq.com/'):

        # 提取公众号名称
        Official_Account = soup.find("a", {"id": "js_name"}).text.strip()

        # 提取创建时间 ct: create_time
        script = soup.find("script", text=lambda text: text and "var ct" in text)
        parser = Parser()
        tree = parser.parse(script.text)
        for node in nodevisitor.visit(tree):
            if isinstance(node, ast.VarDecl) and node.identifier.value == 'ct':
                ct = node.initializer.value
        ct = int(ct.strip('"'))
        create_date = datetime.utcfromtimestamp(ct).strftime('%Y-%m-%d')

        # 提取文章标题、作者和描述信息
        def get_meta(soup, meta):
            raw = soup.find("meta", property=meta)
            meta = raw['content'] if raw else ""
            return meta

        title = get_meta(soup, "og:title")
        author = get_meta(soup, "og:article:author")
        description = get_meta(soup, "og:description")

    elif "zhihu.com" in message.text:
        Official_Account = "小肚鸡肠的知乎"
        create_date = ""
        title = soup.title.text.strip() + "-" + str(random.randrange(2, 50000000))
        author = "知乎小管家去死"
        description = "知乎删贴还不让别人存档。"

    else:
        Official_Account = ""
        create_date = ""
        title = soup.title.text.strip()
        author = ""
        description = ""


    # 调用系统命令 monolith，保存网页。需要系统已经安装 monolith。
    subprocess.call(["monolith", url, '-o', '/srv/web/mono/' + title + '.html'])

    # 将保存的网址返回，注意需要将中文 url 做编码，否则遇到特殊字符会识别错误
    reply_url = 'http://206.189.252.32:8083/'  + urllib.parse.quote(title) + '.html'
    bot.reply_to(message, reply_url)

    # 保存到 archive.org，archive.today
    try:
        reply_ia = archivenow.push(url, 'ia')[0]
        bot.reply_to(message, reply_ia)
        reply_is = archivenow.push(url, 'is')[0]
        bot.reply_to(message, reply_is)
    except Exception as e:
        bot.reply_to(message, 'oooops, please send the url again.')

    bot.reply_to(message, 'http://206.189.252.32:8085/')

    reply_ia_link = '<a href="' + reply_ia + '" target="_blank">' + '备份3' + '</a>'
    reply_is_link = '<a href="' + reply_is + '" target="_blank">' + '备份2' + '</a>'
    monolith_link = '<a href="' + reply_url + '" target="_blank">' + '备份1' + '</a>'
    message_link = '<a href="' + url + '" target="_blank">' + 'url' + '</a>'

    with open('/srv/web/archive_web3/data/archive.csv', 'a') as csvfile:
        fieldnames = ['提交时间', '帐号', '标题', '发布日期', '描述', '原始链接', '2049bbs','archive.today', 'archive.org']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'提交时间': time.ctime(),
        '帐号': Official_Account,
        '标题': title,
        '发布日期': create_date,
        '描述': description,
        '原始链接': message_link,
        '2049bbs': monolith_link,
        'archive.today': reply_is_link,
        'archive.org': reply_ia_link
        })

# debug 环境
#bot.polling(none_stop=True, timeout=123)

# 生产环境
while True:
    try:
        bot.polling(none_stop=True, timeout=123)
    except Exception as e:
        logger = telebot.logger
        logger.error(e)
        time.sleep(15)

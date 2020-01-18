import datetime
import telebot
import time
import requests
from archivenow import archivenow
from bs4 import BeautifulSoup
import os
import random
bot = telebot.TeleBot("TOKEN", threaded=False)


@bot.message_handler(
    regexp="(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])")
def echo_all(message):

    if 'weibo.com' in message.text or 'weibo.cn' in message.text:
        try:
            bot.reply_to(message, "archive doesn't support weibo")
        except Exception as e:
            bot.reply_to(message, 'oooops, please send the url again.')
    else:
        if message.text.startswith('https://mp.weixin.qq.com/') and '__biz=' in message.text:
            url = '&'.join(message.text.split('&', 5)[:5])
        else:
            url = message.text
        headers={"User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
 		 "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		  "Accept-Language" : "en-us",
  	       	"Connection" : "keep-alive",
  		"Accept-Charset" : "GB2312,utf-8;q=0.7,*;q=0.7"}
        html = requests.get(url, headers = headers)
        soup = BeautifulSoup(html.text, "html.parser")
        if len(soup) == 0:
            Title = datetime.datetime.now().strftime("%Y-%m-%d-") + str(random.randrange(2, 50000000))
        else:
            if message.text.startswith('https://mp.weixin.qq.com/s'):
                Title = soup.h2.text.strip()
            elif "zhihu.com" in message.text:
                Title = soup.title.text.strip() + "-" + str(random.randrange(2, 50000000))
            else:
                Title = soup.title.text.strip()
        Title = Title.replace('\n','')
        Title = Title.replace('|',' ')
        Title = Title.replace('<',' ')
        Title = Title.replace('>',' ')
        Title = Title.replace(',',' ')
        Title = Title.replace(' ','_')

        cmd = 'monolith ' + url + ' -o /srv/web/mono/' + Title + '.html'
        os.system(cmd)
        reply_url = 'http://206.189.252.32:8083/'  + Title + '.html'
        bot.reply_to(message, reply_url)


        try:
            reply_ia = archivenow.push(url, 'ia')[0]
            bot.reply_to(message, reply_ia)
        except Exception as e:
            bot.reply_to(message, 'oooops, please send the url again.')




        with open('archive.csv', 'a') as f1:
            print(reply_ia)
            f1.write(time.ctime() + ',' + message.text + ',' + reply_ia + ',')
            f1.write(Title)
            f1.write('\n')

while True:
    try:
        bot.polling(none_stop=True, timeout=123)
    except Exception as e:
        logger = telebot.logger
        logger.error(e)
        time.sleep(15)

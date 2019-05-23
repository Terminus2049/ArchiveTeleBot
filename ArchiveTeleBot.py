import telebot
import time
import requests
from archivenow import archivenow
from bs4 import BeautifulSoup

bot = telebot.TeleBot("TOKEN", threaded=False)


@bot.message_handler(
    regexp="(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])")
def echo_all(message):
    
    if message.text.startswith('https://mp.weixin.qq.com/s?__biz='):
        reply_text = '&'.join(message.text.split('&', 4)[:4])
        reply = archivenow.push(reply_text, 'is')[0]
    else:
        reply = archivenow.push(message.text, 'is')[0]
        
    if 'weibo.com' in message.text or 'weibo.cn' in message.text:
        try:
            bot.reply_to(message, "archive doesn't support weibo")
        except Exception as e:
            bot.reply_to(message, 'oooops, please send the url again.')
    else:
        try:
            bot.reply_to(message, reply)
        except Exception as e:
            bot.reply_to(message, 'oooops, please send the url again.')

        html = requests.get(message.text)
        soup = BeautifulSoup(html.text, "html.parser")
        if message.text.startswith('https://mp.weixin.qq.com/s'):
          Title = soup.h2.text.strip()
        else:
          Title = soup.title.text.strip()

        with open('archive.csv', 'a') as f1:
            f1.write(time.ctime() + ',' + message.text + ',' + reply + ',')
            f1.write(Title)
            f1.write('\n')


while True:
    try:
        bot.polling(none_stop=True, timeout=123)
    except Exception as e:
        logger = telebot.logger
        logger.error(e)
        time.sleep(15)

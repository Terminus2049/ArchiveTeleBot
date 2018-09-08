import telebot
import archiveis
import logging
import time
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot("TOKEN", threaded=False)

@bot.message_handler(regexp="(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])")
def echo_all(message):
	reply = archiveis.capture(message.text)
	bot.reply_to(message, reply)

        html = requests.get(message.text)
        Soup = BeautifulSoup(html.text, "html.parser")

	with open('archive.txt', 'a') as f:
		f.write(time.ctime() + '\n' + message.text + '\n' + reply)
        with open('archive.txt', 'a') as f:
            f.write('\n' + '\n')
            with open('archive.txt', 'a') as f:
                f.write(Soup.title.text.encode('utf-8'))


while True:
    try:
        bot.polling(none_stop=True, timeout=123)
    except Exception as e:
	logger = telebot.logger
        logger.error(e)
        time.sleep(15)

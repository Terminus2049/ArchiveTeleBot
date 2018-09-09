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
	Title = BeautifulSoup(html.text, "html.parser").title.text.encode('utf-8').strip()

	with open('archive.csv', 'a') as f1:
		f1.write(time.ctime() + ',' + message.text + ',' + reply + ',')
		f1.write(Title)
		f1.write('\n')

	with open('archive.txt', 'a') as f2:
		f2.write(time.ctime() + '\n' + message.text + '\n' + reply + '\n')
		f2.write(Title)
		f2.write('\n' + '\n')

while True:
    try:
        bot.polling(none_stop=True, timeout=123)
    except Exception as e:
		logger = telebot.logger
        	logger.error(e)
        	time.sleep(15)

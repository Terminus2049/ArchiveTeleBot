import telebot
import archiveis
import logging
import time

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(regexp="(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])")
def echo_all(message):
	reply = archiveis.capture(message.text)
	bot.reply_to(message, reply)
	with open('archive.txt', 'a') as f:
		f.write(time.ctime() + '\n' + message.text + '\n' + reply + '\n' + '\n')


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
	logger = telebot.logger
        logger.error(e)
        time.sleep(15)

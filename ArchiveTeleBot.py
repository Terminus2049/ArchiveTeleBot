import telebot
import archiveis
import logging
import time

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(regexp="(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])")
def echo_all(message):
	bot.reply_to(message, archiveis.capture(message.text))

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
	logger = telebot.logger
        logger.error(e)
        time.sleep(15)

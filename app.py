# Code based on tutorial form Toptal 
# https://www.toptal.com/python/telegram-bot-tutorial-python

# import everything
import re
from flask import Flask, request
import telegram

from datetime import datetime
import pytz

import telebot.actions as actions
from telebot.credentials import bot_token, bot_user_name, URL, allowed_unames

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

# start the flask app
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
	# retrieve the message in JSON and then transform it to Telegram object
	update = telegram.Update.de_json(request.get_json(force=True), bot)

	# get current timezone - should be moved to actions
	timezone = pytz.timezone('America/Argentina/Buenos_Aires')
	print(timezone.localize(datetime.now()))

	try:
		chat_id = update.message.chat.id
		msg_id = update.message.message_id
		sender_uname = update.message.from_user['username']
	except AttributeError:
		# cannot send a message, exiting
		return 'error'

	# Only allowed usernames can talk to the bot
	if sender_uname not in allowed_unames:
		# send a rejection message
		actions.send_message(bot, chat_id, msg_id, "You are not allowed to talk to me")

		return 'ok'

	# Telegram understands UTF-8, so encode text for unicode compatibility
	text = update.message.text.encode('utf-8').decode()

	msg_obj = actions.Message(bot, chat_id, msg_id, sender_uname, text)

	# for debugging purposes only
	print("got text message :", text)

	args_vec = text.split()
	command = args_vec[0]

	# start()
	if command == "/start":
		actions.start(msg_obj)

	# book(from: datetime, to: datetime, certain: bool = True)
	elif command == "/book":
		if len(args_vec) < 3:
			# send a missing params message
			actions.send_message(bot, chat_id, msg_id, "Missing arguments")
			return 'ok'

		actions.book(
			msg_obj, 
			actions.get_datetime(args_vec[1]), 
			actions.get_datetime(args_vec[2]), 
			False if len(args_vec) >= 4 and args_vec[3].lower() == 'false' else True
		)
	
	# get_booked(from: date)
	elif command == "/getBooked":
		if len(args_vec) < 2:
			# send a missing params message
			actions.send_message(bot, chat_id, msg_id, "Missing arguments")
			return 'ok'

		actions.get_booked(msg_obj, actions.get_datetime(args_vec[1]))
	
	# unbook(from: datetime)
	elif command == "/unbook":
		if len(args_vec) < 2:
			# send a missing params message
			actions.send_message(bot, chat_id, msg_id, "Missing arguments")
			return 'ok'

		actions.unbook(msg_obj, actions.get_datetime(args_vec[1]))

	# my_booked()
	elif command == "/myBooked":
		actions.my_booked(msg_obj)

	else:
		# send a welcoming message
		actions.send_message(bot, chat_id, msg_id, "Invalid command")

	return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
	# we use the bot object to link the bot to our app which live
	# in the link provided by URL
	s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
	# something to let us know things work
	if s:
		return "webhook setup ok"
	else:
		return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)

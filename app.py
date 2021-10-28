# Code based on tutorial from Toptal 
# https://www.toptal.com/python/telegram-bot-tutorial-python
# And tutorial from MongoDB
# https://www.mongodb.com/developer/how-to/use-atlas-on-heroku/

# import everything
import re
import os
from flask import Flask, request
import telegram
import pymongo

import telebot.actions as actions
from telebot.credentials import bot_token, bot_user_name, URL, allowed_unames

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

# start the flask app
app = Flask(__name__)

# connecting to MongoDB
mongodb_url = os.environ.get('MONGODB_URI', None)
if not mongodb_url:
	mongodb_url = "mongodb+srv://username:password@booketioseast.h4nxa.mongodb.net/database?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongodb_url)
db = client.bookings

# MongoDB documentes will be in the form
# {
# 	'_id': Date(beg_date),
# 	'end': Date(end_date),
# 	'username': 'username',
# 	'confirmed': true
# }
# create secondary index for end in collection 'etios'
db.etios.create_index([("end", pymongo.DESCENDING)])

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
	# retrieve the message in JSON and then transform it to Telegram object
	update = telegram.Update.de_json(request.get_json(force=True), bot)

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
		actions.send_message(bot, chat_id, msg_id, "👮 You are not allowed to talk to me")

		return 'ok'

	# Telegram understands UTF-8, so encode text for unicode compatibility
	text = update.message.text.encode('utf-8').decode().lower()

	msg_obj = actions.Message(bot, chat_id, msg_id, sender_uname, text)

	# for debugging purposes only
	print("got text message :", text)

	args_vec = text.split()
	command = args_vec[0]

	# start()
	if command == "/start" or command == "/help":
		actions.start(db, msg_obj)

	# book(from: datetime, to: datetime, certain: bool = True)
	elif command == "/book":
		if len(args_vec) < 3:
			# send a missing params message
			actions.send_message(bot, chat_id, msg_id, "❌ Missing arguments ❌")
			return 'ok'

		try:
			beg_date = actions.get_datetime(args_vec[1])
			end_date = actions.get_datetime(args_vec[2])
		except ValueError:
			# send a missing params message
			actions.send_message(bot, chat_id, msg_id, "❌ Invalid dates ❌")
			return 'ok'

		actions.book(
			db,
			msg_obj, 
			beg_date, 
			end_date, 
			False if len(args_vec) >= 4 and args_vec[3] == 'false' else True
		)
	
	# get_booked(from: date)
	elif command == "/getbooked":
		if len(args_vec) < 2:
			# send a missing params message
			actions.send_message(bot, chat_id, msg_id, "❌ Missing arguments ❌")
			return 'ok'

		try:
			beg_date = actions.get_datetime(args_vec[1])
		except ValueError:
			# send a missing params message
			actions.send_message(bot, chat_id, msg_id, "❌ Invalid date ❌")
			return 'ok'

		actions.get_booked(db, msg_obj, beg_date)
	
	# unbook(from: datetime)
	elif command == "/unbook":
		if len(args_vec) < 2:
			# send a missing params message
			actions.send_message(bot, chat_id, msg_id, "❌ Missing arguments ❌")
			return 'ok'

		try:
			beg_date = actions.get_datetime(args_vec[1])
		except ValueError:
			# send a missing params message
			actions.send_message(bot, chat_id, msg_id, "❌ Invalid date ❌")
			return 'ok'

		actions.unbook(db, msg_obj, beg_date)

	# confirm(from: datetime)
	elif command == "/confirm":
		if len(args_vec) < 2:
			# send a missing params message
			actions.send_message(bot, chat_id, msg_id, "❌ Missing arguments ❌")
			return 'ok'

		try:
			beg_date = actions.get_datetime(args_vec[1])
		except ValueError:
			# send a missing params message
			actions.send_message(bot, chat_id, msg_id, "❌ Invalid date ❌")
			return 'ok'

		actions.confirm(db, msg_obj, beg_date)

	# my_booked()
	elif command == "/mybooked":
		actions.my_booked(db, msg_obj)

	else:
		# send a welcoming message
		actions.send_message(bot, chat_id, msg_id, "❌ Invalid command ❌")

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

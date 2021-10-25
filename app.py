# Code based on tutorial form Toptal 
# https://www.toptal.com/python/telegram-bot-tutorial-python

# import everything
import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL

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

	print("update:", update)
	# 2021-10-25T17:22:32.990375+00:00 app[web.1]: update: {'message': {'delete_chat_photo': False, 'photo': [], 
	# 'chat': {'type': 'private', 'first_name': 'Julián', 'username': 'jtallar', 'last_name': 'Tallar', 'id': 1533769371}, 
	# 'channel_chat_created': False, 'group_chat_created': False, 'caption_entities': [], 'text': 'Message', 
	# 'date': 1635182552, 'entities': [], 'new_chat_photo': [], 'new_chat_members': [], 'message_id': 9, 
	# 'supergroup_chat_created': False, 
	# 'from': {'username': 'jtallar', 'is_bot': False, 'last_name': 'Tallar', 'id': 1533769371, 'language_code': 'es', 
	# 	'first_name': 'Julián'}}, 
	# 'update_id': 959213294}

	chat_id = update.message.chat.id
	msg_id = update.message.message_id
	sender_uname = update.message['from'].username

	# Check if sender is jtallar or nicoManija
	if sender_uname != 'jtallar' and sender_uname != 'nicoManija':
		# send a rejection message
		reject_message = "You are not allowed to talk to me"
		bot.sendChatAction(chat_id=chat_id, action="typing")
		bot.sendMessage(chat_id=chat_id, text=reject_message, reply_to_message_id=msg_id)

		return 'ok'

	# Telegram understands UTF-8, so encode text for unicode compatibility
	text = update.message.text.encode('utf-8').decode()
	# for debugging purposes only
	print("got text message :", text)
	# the first time you chat with the bot AKA the welcoming message
	if text == "/start":
		# print the welcoming message
		bot_welcome = """
		Welcome to coolAvatar bot, the bot is using the service from http://avatars.adorable.io/ to generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with an avatar for your name.
		"""
     	# send the welcoming message
		bot.sendChatAction(chat_id=chat_id, action="typing")
		bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

	else:
		try:
			# clear the message we got from any non alphabets
			text = re.sub(r"\W", "_", text)
			# create the api link for the avatar based on http://avatars.adorable.io/
			url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
			# reply with a photo to the name the user sent,
			# note that you can send photos by url and telegram will fetch it for you
			bot.sendChatAction(chat_id=chat_id, action="upload_photo")
			bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
		except Exception:
			# if things went wrong
			bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

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

def send_message(bot, chat_id, msg_id, text):
    bot.sendChatAction(chat_id=chat_id, action="typing")
    bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=msg_id)

def send_photo(bot, chat_id, msg_id, photo_url):
    # note that you can send photos by url and telegram will fetch it for you
    bot.sendChatAction(chat_id=chat_id, action="upload_photo")
    bot.sendPhoto(chat_id=chat_id, photo=photo_url, reply_to_message_id=msg_id)
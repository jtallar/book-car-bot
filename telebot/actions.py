from datetime import datetime

class Message(object):
    def __init__(self, bot, chat_id, msg_id, sender_uname, text):
        self.bot = bot
        self.chat_id = chat_id
        self.msg_id = msg_id
        self.sender_uname = sender_uname
        self.text = text

def send_message(bot, chat_id, msg_id, text):
    bot.sendChatAction(chat_id=chat_id, action="typing")
    bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=msg_id)

def send_photo(bot, chat_id, msg_id, photo_url):
    # note that you can send photos by url and telegram will fetch it for you
    bot.sendChatAction(chat_id=chat_id, action="upload_photo")
    bot.sendPhoto(chat_id=chat_id, photo=photo_url, reply_to_message_id=msg_id)

def start(msg_obj: Message):
    bot_welcome = """
		Welcome to BookEtios bot, available commands are: \n
        - /book from to [certain] --> /book 2021-10-25T00:05:00 2021-10-25T00:09:00 true
        - /getBooked from --> /getBooked 2021-10-25
        - /unbook from --> /unbook 2021-10-25
        - /myBooked --> /myBooked
		"""
    send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, bot_welcome)

def book(msg_obj: Message, beg: datetime, end: datetime, certain: bool = True):
    print(f'Args - beg: {beg} - end: {end} - certain: {certain}')
    # Check if beg < end

    # Check if slot is available

    # Book slot

    # Send book confirmation

    send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Not implemented (yet)")

def get_booked(msg_obj: Message, beg: datetime):
    print(f'Args - beg: {beg}')
    # Get beg's booked

    send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Not implemented (yet)")

def unbook(msg_obj: Message, beg: datetime):
    print(f'Args - beg: {beg}')
    # Check if beg is booked by msg_obj.sender_uname

    # Unbook slot

    send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Not implemented (yet)")

def my_booked(msg_obj: Message):
    # Get msg_obj.sender_uname booked

    send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Not implemented (yet)")

# TODO: Add today, tomorrow, etc
def get_datetime(text: str):
    return datetime.fromisoformat(text)
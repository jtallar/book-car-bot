from datetime import datetime, timedelta
import pytz
import pymongo

# get current timezone
timezone = pytz.timezone('America/Argentina/Buenos_Aires')

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

def start(db, msg_obj: Message):
    bot_welcome = """
		Welcome to BookEtios bot, available commands are: \n
        - /book from to [certain] --> /book 2021-10-25T00:05:00 2021-10-25T00:09:00 false
        - /getBooked from --> /getBooked 2021-10-25
        - /unbook from --> /unbook 2021-10-25T00:05:00
        - /myBooked --> /myBooked
        - /confirm from --> /confirm 2021-10-25T00:05:00
		"""
    send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, bot_welcome)

def book(db, msg_obj: Message, beg: datetime, end: datetime, certain: bool = True):
    print(f'Args - beg: {beg} - end: {end} - certain: {certain}')

    now_date = get_now_datetime()

    # Check if beg < end and beg >= now
    if beg >= end or beg < now_date:
        send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Invalid dates")
        return

    # Check if slot is available
    ## Find collision with new slot
    ## Slot is not available if exists X such that
    ### (begPrevX <= beg <= endPrevX) ||
    ### (begPrevX <= end <= endPrevX) ||
    ### (beg <= begPrevX <= end) ||
    ### (beg <= endPrevX <= end)
    collision_count = db.etios.find({ 
        "$or": [  
            { "$and": [  
                { "_id" : { "$lte": beg } }, 
                { "end" : { "$gte": beg } } 
            ] }, 
            { "$and": [  
                { "_id" : { "$lte": end } }, 
                { "end" : { "$gte": end } } 
            ] }, 
            { "$and": [  
                { "_id" : { "$gte": beg } }, 
                { "_id" : { "$lte": end } } 
            ] }, 
            { "$and": [  
                { "end" : { "$gte": beg } }, 
                { "end" : { "$lte": end } } 
            ] } 
        ] }).count()

    print(f'Collided: {collision_count}')

    # If collisions exist, cannot book
    if collision_count > 0:
        send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Collision with other bookings!")
        return

    # Book slot
    ## Insert into MongoDB
    insert_resp = db.etios.insert_one({
        "_id": beg, "end": end, 
        "username": msg_obj.sender_uname, "confirmed": certain
    })

    if not insert_resp.inserted_id:
        send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Error inserting, try again later!")
        return

    # Send book confirmation
    send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Etios booked successfully!")

def get_booked(db, msg_obj: Message, beg: datetime):
    print(f'Args - beg: {beg}')
    # Get beg's booked
    ## Find all booked from beg to beg+1
    
    end = beg + timedelta(days=1)

    bookings = db.etios.find({
        "$or": [   
            {  "$and": [
                { "_id" : { "$gte": beg } },  
                { "_id" : { "$lte": end } } 
            ] },  
            { "$and": [   
                { "end" : { "$gte": beg } },  
                { "end" : { "$lte": end } } 
            ] }
        ] }).sort({ "_id": 1 })

    print("Get bookings response: ")
    print(bookings)

    # TODO: I will need to convert from UTC to here
    # TODO: Build message with all bookings
    send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Not implemented (yet)")

def unbook(db, msg_obj: Message, beg: datetime):
    print(f'Args - beg: {beg}')
    # Check if beg is booked by msg_obj.sender_uname
    ## Find one with beg
    ## Check owner

    # Unbook slot
    ## Delete from MongoDB
    ### Could be a delete IF? And avoid the get

    send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Not implemented (yet)")

def my_booked(db, msg_obj: Message):
    # Get msg_obj.sender_uname booked
    ## Find all by username from the future

    send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Not implemented (yet)")

def confirm(db, msg_obj: Message, beg: datetime):
    # Get msg_obj.sender_uname booked
    ## Find one with beg
    ## Check owner

    # Confirm slot
    ## Modify from MongoDB
    ### Could be a modify IF? And avoid the get

    send_message(msg_obj.bot, msg_obj.chat_id, msg_obj.msg_id, "Not implemented (yet)")

def get_datetime(text: str):
    if text == 'today' or text == 'hoy':
        return get_now_datetime() + timedelta(minutes=1)
    elif text == 'tomorrow' or text == 'mañana':
        return get_now_datetime() + timedelta(days=1)
    elif text == 'day after tomorrow' or text == 'pasado':
        return get_now_datetime() + timedelta(days=2)

    return timezone.localize(datetime.fromisoformat(text))

def get_now_datetime():
    return datetime.now(timezone)
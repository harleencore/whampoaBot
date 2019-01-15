import json # parse json responses from telegram into python dictionaries
import requests # make web requests using python, interact with telegram API
import time
import urllib
from dbhelper import DBHelper
db = DBHelper()

TOKEN = "679424726:AAFhyVf602gZxaS0pEIfyiVwqOA7KASWbmw"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# download content from URL and give us a string
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

# get a string response, parses into dictionary
def get_json_from_url(url):
    content = get_url(url) # get content from URL with get_url
    js = json.loads(content) # parse into dictionary --> loads = load String
    return js

# fetches a list of updates-- messages sent to Bot
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100" # with long polling
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url) # get UPDATES from URL, parse into dictionary
    return js

# get chat ID and message text of most recent message
# SIMPLE BUT INELEGANT!!
# get_updates() gets ALL recent messages-- we're downloading waaay more
# than neccesary.
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


# takes text message and chat_id of intended recipient + sends msg
def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        # since we built the entire keyboard object in build_items_keyboard(),
        # we can pass it along to telegram in this function whenever neccesary
        # reply_markup has the keyboard ALONG WITH vals like one_time_keyboard = True
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

# calculates highest ID of all the updates
def get_last_update_id(updates):
    update_ids = []
    # loop through each update and return the biggest ID
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def handle_updates(updates):
    give_feedback = False # by default, you're only viewing
    kid = ""
    subject = ""
    subjects = [] #??????
    for update in updates["result"]: # loop through each update
        try:
            # grab text and chat components
            text = update["message"]["text"] # check message text
            chat = update["message"]["chat"]["id"] # check user who sent msg
            kids = db.get_kids(chat)
            if text == "/feedback":
                keyboard = build_items_keyboard(kids)
                send_message("Select a kid to submit feedback for", chat, keyboard)
                give_feedback = True
            elif text == "/view":
                keyboard = build_items_keyboard(kids)
                send_message("Select a kid to view feedback for", chat, keyboard)
                give_feedback = False
            elif text == "/start":
                send_message("Welcome to the FeedbackBot! Send any text to me and I'll store it as feedback.", chat)
            elif text.startswith("/"):
                continue
            elif text in kids: # if a kid was selected
                kid = text # set current kid
                subjects = db.get_kids(chat, kid)
                keyboard = build_items_keyboard(subjects)
                if give_feedback:
                    send_message("Select a subject to submit feedback for")
                    keyboard = build_items_keyboard(subjects)
                else:
                    send_message("Select a subject to view feedback for")
                    keyboard = build_items_keyboard(subjects)
            elif text in subjects:




            else:
                if subject and kid:
                    db.add_item(text, chat, kid, subject)
                    # observations = db.get_kids(chat) # update kids variable
                    # message = "\n".join(kids) # message is a list of all kids
                    # send_message(message, chat) # print (send) updated list
                else:
                    send_message("Please select a kid and subject first.")


        except KeyError:
            pass

def build_items_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)





# this is so we can import our functions into another script
# without running anything
def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()

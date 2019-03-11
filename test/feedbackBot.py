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
    child = ""
    subject = ""
    subjects = []
    add_child = False
    for update in updates["result"]: # loop through each update
        try:
            # grab text and chat components
            text = update["message"]["text"] # check message text
            chat = update["message"]["chat"]["id"] # check user who sent msg
            children = db.get_children(chat)
            if not add_child:
                if text == "/feedback":
                    keyboard = build_items_keyboard(children)
                    send_message("Select a child to submit feedback for", chat, keyboard)
                    give_feedback = True
                elif text == "/view":
                    keyboard = build_items_keyboard(children)
                    send_message("Select a child to view feedback for", chat, keyboard)
                    give_feedback = False
                elif text == "/addchild":
                    send_message("Please enter the name of the child.", chat)
                    add_child = True
                elif text in children: # if a child was selected
                    child = text # set current child
                    subjects = db.get_subjects(chat, child)
                    keyboard = build_items_keyboard(subjects)
                    if give_feedback:
                        send_message("Select a subject to submit feedback for", chat, keyboard)
                    else:
                        send_message("Select a subject to view feedback for", chat, keyboard)
                elif text in subjects:
                    subject = text
                    if give_feedback:
                        send_message("Adding " + subject +" feedback for " + child)
                        add_feedback(text, chat, child, subject)
                    else:
                        send_message("Showing " + subject + " feedback for " + child)
                        feedback = get_feedback(chat, child, subject)
                        message = "\n".join(feedback)
                        send_message(message, chat)

                elif text == "/start":
                    send_message("Welcome to the FeedbackBot! Send /feedback to submit feedback, or /view to pull up a list of past committed feedback.", chat)
                elif text.startswith("/"):
                    continue
            else:
                db.add_child(chat, text)




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

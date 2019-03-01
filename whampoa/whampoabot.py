import json # parse json responses from telegram into python dictionaries
import requests # make web requests using python, interact with telegram API
import time
import urllib
from dbhelper import DBHelper
db = DBHelper()

TOKEN = "679424726:AAFhyVf602gZxaS0pEIfyiVwqOA7KASWbmw"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


add_child = False
child = ""
feedback_mode = False
admin_mode = False
subjects = ["Math", "Science", "English", "General"]
subject = "General"

# download content from URL and give us a string
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

# get a string response, parses into dictionary
def get_json_from_url(url):
    content = get_url(url) # get content from URL with get_url
    js = json.loads(content)
    return js

# fetches a list of updates-- messages sent to Bot
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100" # with long polling
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
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
    global add_child
    global child
    global feedback_mode
    global admin_mode
    global subjects
    global subject
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            children = db.get_children(chat)

            if not admin_mode:

                if text == "/help":
                    help_message = ("Welcome to the Whampoa feedback bot! Here are the commands you'll need:\n\n"
                    "/sendFeedback : submit feedback for a child\n"
                    "/viewFeedback : view feedback for a child\n"
                    "/setChild : set the child you want to work with\n"
                    "/addChild : add a child to the database\n"
                    "/viewChildren : view all children in the database\n"
                    "/setSubject : set subject\n"
                    "/commands : quick access to most important commands\n"
                    "/cancel : cancel adding comments/ child to database")
                    send_message(help_message, chat)

                if text == "/cancel":
                    send_message("`process cancelled.`", chat)

                if text == "/commands":
                    commands = ("\n"
                    "/setSubject\n"
                    "/setChild\n"
                    "/sendFeedback\n"
                    "/viewFeedback\n"
                    "/cancel")
                    send_message(commands, chat)

                elif text == "/setChild":
                    if children:
                        keyboard = build_items_keyboard(children)
                        send_message("`Select a child`", chat, keyboard)
                    else:
                        send_message("`There are currerntly no children in the database`", chat)

                elif text == "/sendFeedback":
                    if child:
                        send_message("`Please enter " + subject + " feedback for " + child + "`", chat)
                        admin_mode = True
                        feedback_mode = True
                    else:
                        send_message("`Child not selected.`", chat)

                elif text in children:
                    send_message("`Child set to: " + text + "`", chat)
                    child = text

                elif text in subjects:
                    send_message("`Subject set to: " + text + "`", chat)
                    subject = text

                elif text == "/addChild":
                    send_message("`Please enter name`", chat)
                    admin_mode = True
                    add_child = True

                elif text == "/viewFeedback":
                    if child:
                        send_message("`Showing " + subject + " feedback for "+ child + "`", chat)

                        message = ""
                        if subject is not "General":
                            feedback = db.get_feedback(chat, child, subject)

                        else:
                            feedback_array = []
                            for subject in subjects:
                                feedback_array.append(db.get_feedback(chat, child, subject))

                            feedback_check = False
                            for i in range (len(subjects)-1):
                                if feedback_array[i]:
                                    feedback_check = True
                                    message += "*" + subjects[i] + "*\n" + "\n".join(feedback_array[i]) + "\n\n"
                            if feedback_array[3]:
                                message += "*General*\n" + "\n".join(feedback_array[3])
                            else:
                                if not feedback_check:
                                    message = "`Error! No feedback for this child yet!`"

                        if not message:
                            message = "\n".join(feedback)
                        send_message(message, chat)
                    else:
                        send_message("`Child not selected.`", chat)

                elif text == "/viewChildren":
                    message = '\n'.join(children)
                    if not message:
                        message = "`There are no children in the database!`"
                    send_message(message, chat)

                elif text == "/setSubject":
                    keyboard = build_items_keyboard(subjects)
                    send_message("`Select a subject`", chat, keyboard)
            else:

                if text == "/cancel":
                    send_message("`process cancelled`", chat)
                    add_child = False
                    admin_mode = False
                    feedback_mode = False

                if add_child:
                    db.add_child(text, chat)
                    add_child = False
                    admin_mode = False
                    send_message("`"+ text+" added to database`", chat)

                if feedback_mode:
                    db.add_feedback(text, chat, child, subject)
                    send_message("`Feedback saved!`", chat)
                    feedback_mode = False
                    admin_mode = False


        except KeyError:
            pass


def build_items_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

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

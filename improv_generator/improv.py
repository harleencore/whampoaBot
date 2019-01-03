import json # parse json responses from telegram into python dictionaries
import requests # make web requests using python, interact with telegram API
import time

TOKEN = "586549666:AAHgb31bgnRj-ZmdKj2DDmYt_Us6OpfAK1o"
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
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
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
def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

# calculates highest ID of all the updates
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

# echo reply for each message that we receieve
def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


# this is so we can import our functions into another script
# without running anything
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()

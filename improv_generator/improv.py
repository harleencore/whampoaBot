# import telepot
import json # parse json responses from telegram into python dictionaries
import requests # make web requests using python, interact with telegram API

#
# TelegramBot = telepot.Bot(token)
# print( TelegramBot.getMe())
#
# print(TelegramBot.getUpdates(33894979+1))

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
def get_updates():
    url = URL + "getUpdates"
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


text, chat = get_last_chat_id_and_text(get_updates())
send_message(text, chat)

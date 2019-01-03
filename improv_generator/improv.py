import telepot
token = '586549666:AAHgb31bgnRj-ZmdKj2DDmYt_Us6OpfAK1o'
TelegramBot = telepot.Bot(token)
print( TelegramBot.getMe())

print(TelegramBot.getUpdates(33894979+1))

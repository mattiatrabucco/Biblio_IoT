# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import os
import django
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioSite.settings')
django.setup()

import telebot
from myapp.models import TessereUnimore
from myapp.views import where_to_go

API_TOKEN = config("TELEGRAM_SECRET_KEY")

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.add(telebot.types.KeyboardButton(text="Bot, mostrami la miglior biblioteca in cui andare adesso"))

    if message.from_user.username is None:
        bot.reply_to(message, """\
Ciao, sono il bot di Biblio IoT!

Per funzionare correttamente devi possedere un nome utente Telegram e impostarlo nell'area riservata del nostro sito. \
""", reply_markup=keyboard)
    else:
        bot.reply_to(message, """\
Ciao, sono il bot di Biblio IoT!

Per funzionare correttamente ricordati di impostare il tuo username Telegram nell'area riservata del nostro sito.\
""", reply_markup=keyboard)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def message(message):
    
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.add(telebot.types.KeyboardButton(text="Bot, mostrami la miglior biblioteca in cui andare adesso"))
    #keyboard.add(telebot.types.KeyboardButton(text="Ciao 2"))
    '''menu1 = telebot.types.InlineKeyboardMarkup()
    menu1.add(telebot.types.InlineKeyboardButton(text = 'Prova 1', callback_data ='first'))
    menu1.add(telebot.types.InlineKeyboardButton(text = 'Prova 2', callback_data ='second'))
    msg = bot.send_message(message.chat.id, text ='Ciao', reply_markup = menu1)'''

    if message.text == 'Bot, mostrami la miglior biblioteca in cui andare adesso':
        #msg = bot.send_message(message.chat.id, text ='boooh', reply_markup = menu1)
        #bot.register_next_step_handler(msg, step2)
        #bot.reply_to(message, (message.text + str(where_to_go(TessereUnimore.objects.get(telegram_id="trabosamba")))))
        dove_andare = str(where_to_go(TessereUnimore.objects.get(telegram_id="trabosamba"))).upper()
        risposta = f"La miglior biblioteca in cui andare ora è: { dove_andare }"
        bot.send_message(message.chat.id, risposta, reply_markup=keyboard)
    else:
         bot.send_message(message.chat.id, "Sono spiacente, il comando non è supportato", reply_markup=keyboard)


bot.polling()
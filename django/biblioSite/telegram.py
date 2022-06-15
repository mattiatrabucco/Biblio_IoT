# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import os
from re import M
import django
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioSite.settings')
django.setup()

import telebot
from myapp.models import TessereUnimore
from myapp.views import where_to_go, redeem_reward

API_TOKEN = config("TELEGRAM_SECRET_KEY")
API_URL = "http://192.168.75.123:8000"

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    #keyboard = telebot.types.ReplyKeyboardMarkup()
    #keyboard.add(telebot.types.KeyboardButton(text="Bot, mostrami la miglior biblioteca in cui andare adesso"))

    if message.from_user.username is None:
        bot.send_message(message.chat.id, """\
Ciao, sono il bot di Biblio IoT!

N.B.: per funzionare correttamente devi possedere un nome utente Telegram e impostarlo nell'area riservata del nostro sito.

Premi /help per saperne di più.\
""")
    else:
        bot.send_message(message.chat.id, """\
Ciao, sono il bot di Biblio IoT!

Per funzionare correttamente ricordati di impostare il tuo username Telegram nell'area riservata del nostro sito.

Premi /set per impostare il nome utente sul nostro sito (devi averlo già su Telegram).
Premi /bestbiblio per ottenere il suggerimento della miglior biblioteca in cui andare ora.
Premi /reward per ottenere il reward del giorno.
Premi /help per saperne di più.\
""")

# Handle '/help'
@bot.message_handler(commands=['help'])
def send_help(message):
    if message.from_user.username is None:
        bot.send_message(message.chat.id, """\
Ciao! Se vuoi che tutto funzioni correttamente, devo sapere chi sei.

Attualmente non hai un nome_utente Telegram, ma puoi rimediare! Sceglilo ora nelle impostazioni dell'app, poi torna qui e premi ancora una volta /help.\
""")
    else:
        bot.send_message(message.chat.id, f"""\
Ciao {message.from_user.username},

hai già associato il nome_utente Telegram al tuo profilo nel nostro sito? Se non l'hai ancora fatto, premi /set.


Devo ancora imparare tantissimo, ma per ora posso aiutarti a:

- Ottenere il suggerimento della miglior biblioteca in cui andare ora, premendo /bestbiblio.
- Ottenere il reward del giorno se sei andato nella biblioteca consigliata, premendo /reward.\
""")

# Handle '/bestbiblio'
@bot.message_handler(commands=['bestbiblio'])
def send_bestbiblio(message):
    if message.from_user.username is None:
        bot.send_message(message.chat.id, """\
Ciao! Se vuoi che tutto funzioni correttamente, devo sapere chi sei.

Attualmente non hai un nome_utente Telegram, ma puoi rimediare! Sceglilo ora nelle impostazioni dell'app, poi torna qui e premi /help.\
""")
    else:
        dove_andare = str(where_to_go(TessereUnimore.objects.get(telegram_id=message.from_user.username))).upper()
        bot.send_message(message.chat.id, f"""\
Secondo i miei calcoli, la miglior biblioteca in cui andare adesso è: 
            
*{ dove_andare }*\
""", parse_mode="MARKDOWN")

# Handle '/reward'
@bot.message_handler(commands=['reward'])
def send_reward(message):
    if message.from_user.username is None:
        bot.send_message(message.chat.id, """\
Ciao! Se vuoi che tutto funzioni correttamente, devo sapere chi sei.

Attualmente non hai un nome_utente Telegram, ma puoi rimediare! Sceglilo ora nelle impostazioni dell'app, poi torna qui e premi /help.\
""")
    else:
        try:
            utente = TessereUnimore.objects.get(telegram_id=message.from_user.username)
        except (TessereUnimore.DoesNotExist):
            bot.send_message(message.chat.id, "Ciao! Sei sicuro di aver impostato correttamente il tuo nome_utente Telegram sul nostro sito web? Controlla ora premendo /set.")
            return
        
        reward = redeem_reward(utente)
        if reward == "DONE":
            bot.send_message(message.chat.id, "Reward di oggi riscattato correttamente!")
        elif reward == "ALREADY":
            bot.send_message(message.chat.id, "Il reward di oggi è già stato riscattato.")
        else:
            bot.send_message(message.chat.id, "Reward non riscattato. Sei sicuro di essere entrato nella biblioteca suggerita?")

# Handle '/set'
@bot.message_handler(commands=['set'])
def send_set(message):
    
    bot.send_message(message.chat.id, f"Visita l'area riservata del nostro sito <a href='{API_URL}/home'>premendo qui</a>", parse_mode="HTML")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def message(message):
    
    '''keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.add(telebot.types.KeyboardButton(text="Mostrami la miglior biblioteca in cui andare adesso"))
    keyboard.add(telebot.types.KeyboardButton(text="Fammi ottenere il reward di oggi"))
    #keyboard.add(telebot.types.KeyboardButton(text="Ciao 2"))
    menu1 = telebot.types.InlineKeyboardMarkup()
    menu1.add(telebot.types.InlineKeyboardButton(text = 'Prova 1', callback_data ='first'))
    menu1.add(telebot.types.InlineKeyboardButton(text = 'Prova 2', callback_data ='second'))
    msg = bot.send_message(message.chat.id, text ='Ciao', reply_markup = menu1)'''

    bot.send_message(message.chat.id, "Sono spiacente, il comando non è supportato. Prova con /help")


bot.polling()
import telebot
import functions
from constants import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def command_help(message):
    bot.send_message(message.chat.id, "Список команд:\n"
                          "/start - start\n"
                          "/help - help\n"
                                      "/roll - Случайное число от 0 до 100\t/roll {number}\n"
                                      "/flip")

@bot.message_handler(commands=['flip'])
def command_flip(message):
    my_flip = functions.flip()
    bot.reply_to(message, my_flip)

@bot.message_handler(commands=["roll"])
def command_roll(message):
    num = message.text.split(' ')
    if len(num) == 1:
        my_roll = functions.roll()
        bot.reply_to(message, my_roll)
    elif len(num) == 2:
        num = num[-1]
        my_roll = functions.roll(int(num))
        bot.reply_to(message, my_roll)
    else:
        bot.reply_to(message, 'Invalid syntax! Try: "/roll {number}"')
@bot.message_handler(commands=["reg"])
def command_register(message):
    user_name = message.from_user.username
    chat_id = message.chat.id
    if functions.register(user_name, chat_id) == False:
        bot.send_message(message.chat.id, "@" + user_name + " уже зарегистрирован!")
    else:
        bot.send_message(message.chat.id, "@" + user_name + " теперь в игре")

@bot.message_handler(commands=["play"])
def command_play(message):
    chat_id = message.chat.id
    user_name = message.from_user.username
    if functions.play(user_name, chat_id) == False:
        bot.send_message(message.chat.id, "Участник не зарегистрирован!\nНапишите /reg для регистрации.")
    else:
        target = functions.play(user_name, chat_id)
        bot_message = 'Сегодняшний герой у нас @' + target
        bot.send_message(message.chat.id, bot_message)

@bot.message_handler(commands=["stats"])
def command_stats(message):
    chat_id = message.chat.id
    data = functions.stats(chat_id)
    for k,v in data.items():
        bot.send_message(message.chat.id, str(k) + " is " + str(v) + " times\n")


bot.polling()

while True: # Don't end the main thread.
    pass

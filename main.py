import telebot
import functions
from constants import TOKEN
import time


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id, "Вас приветствует @dolbaeb_bot!\n"
                                      "\nМеня создали чисто по фану, моё существование не имеет никакого смысла, кроме развлечение отбитых кожаных ублюков вроде тебя :)\n\n"
                                      "Можешь попробовать посмотреть список команд написав /help")

@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(message.chat.id, "Список команд:\n"
                          "/help - Список команд\n"
                                      "/roll - Случайное число от 0 до 100\t\t\t/roll {number}\n"
                                      "/flip - Орёл/решка.\n"
                                      "/reg - Регистрация в игре.\n"
                                      "/play - Запустить игру.\n"
                                      "/add - Добавить реплику для игры\nСообщения расделять знаком '^', ник для сообщения указать '@{}'\t\t\t /add Msg1 ^ msg2 ^ msg3 @{}")

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
    num = functions.play(user_name,chat_id)
    if num[0] == False:
        bot.send_message(message.chat.id, num[1])
    elif num[0] == True:
        response = num[2]
        target = num[1]
        for i in response:
            time.sleep(1)
            bot.send_message(message.chat.id, i.format(target))


@bot.message_handler(commands=["stats"])
def command_stats(message):
    chat_id = message.chat.id
    data = functions.stats(chat_id)
    s = ""
    for k,v in data.items():
        s = s + str(k) + " был пидаром " + str(v) + " раз\n"
    stat_msg = "Топ пидаров:\n\n" + s + "\nВсего участников - {}".format(len(data))
    bot.send_message(message.chat.id, stat_msg)

@bot.message_handler(commands=["add"])
def command_add(message):
    text = message.text
    response_id = functions.add(text)
    bot.send_message(message.chat.id, "Сообщение добавлено! Уникальный идентификатор: " + str(response_id))

bot.polling()

while True: # Don't end the main thread.
    pass

import random
import shelve
from datetime import datetime, date, time

def flip():
    if random.randint(0,1) != 1:
        return "Орел"
    else:
        return "Решка"

def roll(num=100):
    numb = random.randint(0, num)
    return numb


"""----------------------------------------------------------------------------------"""

def register(username, chat_id):
    db_game = shelve.open("game_{}".format(chat_id))
    if username in db_game:
        return False
    else:
        db_game[username] = 0
        db_game.close()
        return True


def play(user_name, chat_id):
    db_date = shelve.open("date_{}".format(chat_id))
    db_game = shelve.open("game_{}".format(chat_id))
    game_list = []
    now = datetime.now().date()

    if user_name not in db_game:
        return False, "Участник не зарегистрирован!\nНапишите /reg для регистрации.",
    elif str(now) not in db_date:
        for k in db_game.keys():
            game_list.append(k)

        target = random.choice(game_list)

        if str(now) not in db_date:
            db_date[str(now)] = target
            count = db_game.pop(target) + 1
            db_game[target] = count
        db_responses = shelve.open("db_responses")
        response_copy = db_responses.pop(str(random.randint(0, len(db_responses)-1)))

        return True, target, response_copy
    else:
        target = db_date[str(now)]
        return False, f"Согласно моей информации, по результатам сегодняшнего розыгрыша пидор дня - @{target}"




    db_game.close()
    db_date.close()


def stats(chat_id):
    db_game = shelve.open("game_{}".format(chat_id))
    stat = {}
    for k,v in db_game.items():
        stat.update({k:v})
    return stat

def today(chat_id):
    db_date = shelve.open("date_{}".format(chat_id))
    now = datetime.now().date()
    if str(now) in db_date:
        target = db_date[str(now)]
        return True, target
    db_date.close()

def add(payload):
    db_responses = shelve.open("db_responses")
    payload = payload[5:].split("/")
    db_responses[str(len(db_responses))] = payload
    id = len(db_responses)
    db_responses.close()

    return id


#register(input("Enter user"))
#name = play("405732032")
#print(name)
#print(stats())
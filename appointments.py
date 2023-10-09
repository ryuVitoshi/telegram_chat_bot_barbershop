from ast import Lambda
from pickle import TRUE
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import credentials
import design
import sqlite3
import texts
import models
import services

bot = credentials.bot
state = models.state
apps_dict = models.apps_dict
apps_buttons = []
services_list = models.services_list

# Fill services
def update_apps_dict(message):
    uid = message.from_user.id
    con = sqlite3.connect(credentials.database)
    c = con.cursor()
    
    c.execute('SELECT * FROM appointments WHERE user=?',(uid,))
    data = c.fetchall()

    if data == None:
        return None
    
    apps_dict[uid] = {}
    for element in data:
        info = {
        'date': element[1],
        'time': element[2],
        'comments': element[3],
        'service': element[4],
        'user': element[5]
        }
        apps_dict[uid] = info
    return apps_dict[uid]
#update_apps_dict(uid)

# My appointments message
@bot.message_handler(func=lambda message: message.text == "📝 My appointments")
def send_my_appointments(message):
    uid = message.from_user.id
    state[uid] = 'myappointments'
    bot.send_message(uid, texts.SIGN_UP, parse_mode='html', reply_markup = keyboard_my_appointments(message))

def keyboard_my_appointments(message):
    uid = message.from_user.id
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    update_apps_dict(message)
    for app in apps_dict[uid]:
        date = app['date']
        time = app['time']
        srvc = app['service']
        text = date+' '+time+''+srvc
        btn = types.KeyboardButton(text)
        menu_keyboard.add(btn)
    btn_sign_up = types.KeyboardButton("➕ Sign up for an appointment")
    btn_back = types.KeyboardButton("⬅️ Back")
    btn_home = types.KeyboardButton("⬆️ Home")
    menu_keyboard.add(btn_sign_up).add(btn_back,btn_home)
    return menu_keyboard

# Sign up message
@bot.message_handler(func=lambda message: message.text == "✍ Sign up" or message.text == "➕ Sign up for an appointment")
def send_sign_up(message):
    uid = message.from_user.id
    state[uid] = 'signup'
    bot.send_message(uid, texts.SIGN_UP, parse_mode='html', reply_markup = services.keyboard_services())

# Choose service to sign up
@bot.message_handler (func=lambda message: message.text in services.services_buttons and
(state[message.from_user.id] == 'signup' or state[message.from_user.id] == 'myappointments'))
def sign_up_choose_service(message):
    uid = message.from_user.id
    text = message.text
    state[uid] = 'signupservice'
    for srvc in services.services_list:
        if srvc['name'] == text:
            bot.send_message(uid, srvc['info'], parse_mode='html', reply_markup = services.keyboard_service(text))
            break

# Choose date to sign up
@bot.message_handler (func=lambda message: message.text in apps_buttons)
def sign_up_choose_date(message):
    uid = message.from_user.id
    text = message.text
    services.services_list[apps_buttons.index(message.text)]
    state[uid] = 'signupdate'
    for srvc in services.services_list:
        if srvc['name'] == text:
            bot.send_message(uid, srvc['info'], parse_mode='html', reply_markup = services.keyboard_service(text))
            break



'''
# Button keyboard for sign up
def keyboard_sign_up(n_cols=2):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(services), n_cols):
        row = services[i:i+n_cols]
        bttns = []
        for item in row:
            bttns.append(types.KeyboardButton(item['name']))
        menu_keyboard.add(*bttns)
    btn_back = types.KeyboardButton("⬅️ Back")
    btn_home = types.KeyboardButton("⬆️ Home")
    menu_keyboard.add(btn_back,btn_home)
    return menu_keyboard
'''

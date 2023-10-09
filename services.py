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
import appointments

bot = credentials.bot
state = models.state
services_list = models.services_list
services_buttons = []

# Fill services
def update_services():
    con = sqlite3.connect(credentials.database)
    c = con.cursor()
    
    c.execute('SELECT * FROM services')
    data = c.fetchall()

    global services_buttons
    global services_list
    if data != None:
        for element in data:
            info = {
            'name': element[1],
            'info': element[2],
            'price': element[3],
            'time': element[4]
            }
            services_list.append(info)
            services_buttons.append(info['name'])
            appointments.apps_buttons.append('✍ Sign up for '+info['name'])
update_services()
#print(services_list)
#print(services_buttons)
#print(appointments.apps_buttons)

# Services message
@bot.message_handler(func=lambda message: message.text == "💇 Services")
def send_services(message):
    uid = message.from_user.id
    state[uid] = 'services'
    bot.send_message(uid, texts.SERVICES, parse_mode='html', reply_markup = keyboard_services())

# Button keyboard for services
def keyboard_services(n_cols=2):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(services_list), n_cols):
        row = services_list[i:i+n_cols]
        bttns = []
        for item in row:
            bttns.append(types.KeyboardButton(item['name']))
        menu_keyboard.add(*bttns)
    btn_back = types.KeyboardButton("⬅️ Back")
    btn_home = types.KeyboardButton("⬆️ Home")
    menu_keyboard.add(btn_back,btn_home)
    return menu_keyboard

# Button keyboard for a specific service
def keyboard_service(srvc):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("✍ Sign up for "+srvc)
    btn_back = types.KeyboardButton("⬅️ Back")
    btn_home = types.KeyboardButton("⬆️ Home")
    menu_keyboard.add(btn1).add(btn_back,btn_home)
    return menu_keyboard

@bot.message_handler (func=lambda message: message.text in services_buttons and state[message.from_user.id] == 'services')
def send_services_info(message):
    uid = message.from_user.id
    text = message.text
    state[uid] = 'service'
    for srvc in services_list:
        if srvc['name'] == text:
            bot.send_message(uid, srvc['info'], parse_mode='html', reply_markup = keyboard_service(text))
            break

    
    #bot.send_message(uid, texts.SERVICES, parse_mode='html', reply_markup = design.keyboard())
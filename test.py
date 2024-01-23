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

from credentials import bot

services_dict = models.services_dict

# Services message
@bot.message_handler(func=lambda message: message.text == '💇 Services')
def send_welcome(message):
    uid = message.from_user.id
    bot.send_message(uid, texts.SERVICES, parse_mode='html', reply_markup = keyboard_services())

services_buttons = ["Master cut","Master long hair","Master beard trim","Master shave","Master head shave","Buzz cut","Kids cut","Braids"]

def keyboard_services():
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Master cut")
    btn2 = types.KeyboardButton("Master long hair")
    btn3 = types.KeyboardButton("Master beard trim")
    btn4 = types.KeyboardButton("Master shave")
    btn5 = types.KeyboardButton("Master head shave")
    btn6 = types.KeyboardButton("Buzz cut")
    btn7 = types.KeyboardButton("Kids cut")
    btn8 = types.KeyboardButton("Braids")
    btn_back = types.KeyboardButton("⬅️ Back")
    btn_home = types.KeyboardButton("⬆️ Home")
    menu_keyboard.add(btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8).add(btn_back,btn_home)
    return menu_keyboard

@bot.message_handler (func=lambda message: message.text in services_buttons)
def send_services_info (message):
    uid = message.from_user.id
    text = message.text
    for srvc in services_dict:
        if srvc['service_name'] == text:
            #apps_dict[]
            bot.send_message(uid, srvc['service_info'], parse_mode='html', reply_markup = design.keyboard())
            break

    
    bot.send_message(uid, texts.SERVICES, parse_mode='html', reply_markup = design.keyboard())
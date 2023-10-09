from ast import Lambda
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import credentials
import texts
import design
import services
import models
import appointments

bot = credentials.bot
state = models.state

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Welcome message"),
    telebot.types.BotCommand("/home", "Welcome message"),
    telebot.types.BotCommand("/services", "Welcome message"),
    telebot.types.BotCommand("/aboutus", "Welcome message"),
    telebot.types.BotCommand("/appointments", "Welcome message"),
    telebot.types.BotCommand("/help", "Information about bot")
])

# Commands

# Welcome message
@bot.message_handler(["start", "home"])
@bot.message_handler(func=lambda message: message.text == '⬆️ Home')
def send_welcome(message):
    uid = message.from_user.id
    state[uid] = 'home'
    photo = open('images/welcome.jpg', 'rb')
    bot.send_photo(uid, photo, caption=texts.WELCOME_TEXT, parse_mode='html', reply_markup = design.keyboard())

# HELP message
@bot.message_handler(["help"])
def send_help(message):
    uid = message.from_user.id
    state[uid] = 'help'
    print(uid)
    pass

# About us message
@bot.message_handler(["aboutus"])
@bot.message_handler(func=lambda message: message.text == "🌎 About us")
def send_info(message):
    uid = message.from_user.id
    state[uid] = 'aboutus'
    button_list = [InlineKeyboardButton("🌐 Our website", url='https://facebook.com')]
    reply_markup = InlineKeyboardMarkup(design.build_menu(button_list, n_cols=1))
    bot.send_message(uid,texts.COMPANY_INFO,parse_mode='html',reply_markup=reply_markup)

# Inline Kayboard Button handler
@bot.callback_query_handler(func=lambda message:True)
def button_press_handler(call):
    data = call.data
    uid = call.from_user.id
    print(data)
    print(uid)
    
    if data == 'test':

        pass

    elif data == '':

        pass

@bot.message_handler(func=lambda message: message.text == '⬅️ Back')
def go_back(message):
    uid = message.from_user.id
    #print(state[uid])
    match state[uid]:
        case 'home':
            send_welcome(message)
        case 'aboutus':
            send_welcome(message)
        case 'help':
            send_welcome(message)
        case 'services':
            send_welcome(message)
        case 'service':
            services.send_services(message)
        case 'signup':
            send_welcome(message)
        case 'myappointments':
            send_welcome(message)
        case 'signupservice':
            appointments.send_sign_up(message)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()
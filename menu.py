from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import texts
import services
import registration
import appointments
import design

from credentials import bot

# Welcome message
@bot.message_handler(["start", "home"])
@bot.message_handler(func=lambda message: message.text == design.menu_navigation[1])
def send_welcome(message):
    user_id = message.from_user.id
    photo = open('images/welcome.jpg', 'rb')
    bot.send_photo(user_id, photo, caption=texts.WELCOME_TEXT, parse_mode='html', reply_markup = design.keyboard(design.menu_options,False,False))
    bot.register_next_step_handler(message, process_menu_selection)

# About us message
def send_info(message):
    user_id = message.from_user.id
    button_list = [InlineKeyboardButton("🌐 Our website", url='https://facebook.com')]
    reply_markup = InlineKeyboardMarkup(design.build_menu(button_list, n_cols=1))
    bot.send_message(user_id,texts.COMPANY_INFO,parse_mode='html')

#
def process_menu_selection(message):
    user_id = message.from_user.id
    choice = message.text
    if choice == design.menu_options[0]:
        services.send_services(message)
    elif choice == design.menu_options[1]:
        send_info(message)
        bot.register_next_step_handler(message, process_menu_selection)
    elif choice == design.menu_options[2]:
        registration.send_profile(message)
    elif choice == design.menu_options[3]:
        appointments.send_appointments(message)
    else:
        bot.register_next_step_handler(message, process_menu_selection)

from ast import Lambda
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import texts
import credentials

bot = credentials.bot

# Key words
start_commands = ["/start", "/help", "/home"]
other_commands = ['/profile', '/aboutus', '/services', '/question']
menu_options = ['💇 Services', '🌎 About us', '✍ Sign up', '📝 My appointments']
menu_hello_options = ['home','hi','hello','start','help','menu','back']
menu_ask_options = ['question','questions','ask','suggestion']
menu_products = ['products','product','service','services']
menu_price_services = ['price', 'prices','cost'] +menu_products
all_keywords = start_commands+other_commands+menu_options+menu_hello_options+menu_ask_options+menu_price_services

#---------------------BUTTONS LAYOUT DESIGN------------------
# Helper function for building a list of buttons in a grid
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

# ----------KEYBOARD MENU----------
# Define keyboard options
def keyboard(n_cols=3):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(menu_options), n_cols):
        row = menu_options[i:i+n_cols]
        menu_keyboard.add(*row)
    btn_back = types.KeyboardButton("⬅️ Back")
    btn_home = types.KeyboardButton("⬆️ Home")
    menu_keyboard.add(btn_back,btn_home)
    return menu_keyboard

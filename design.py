from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from credentials import bot

# Keywords
start_commands = ["/start", "/help", "/home"]
other_commands = ['/profile', '/aboutus', '/services', '/question']
menu_options = ['💇 Services', '🌎 About us', '👩‍🏫 My profile', '📝 My appointments']
menu_navigation = ['⬅️ Back', '⬆️ Home']
menu_change_profile = ['Change Phone Number', 'Change Full Name']

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

# Define custom keyboard
def keyboard(bttns=[], btn_back=True, btn_home=True, n_cols=3):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if not any(isinstance(i, list) for i in bttns):
        bttns = [bttns]
    for elem in bttns:
        for i in range(0, len(elem), n_cols):
            row = elem[i:i+n_cols]
            menu_keyboard.add(*row)
    footer = []
    if btn_back:
        footer.append(types.KeyboardButton(menu_navigation[0]))
    if btn_home:
        footer.append(types.KeyboardButton(menu_navigation[1]))
    menu_keyboard.add(*footer)
    return menu_keyboard
